from dataclasses import dataclass
from typing import Optional
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.encounter import Encounter
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.period import Period
from kafka_fhir_adapter.services.fhir_organization import *
from kafka_fhir_adapter.services.fhir_location import *
from kafka_fhir_adapter.services.fhir import epoch_timestamp_to_iso_string
from kafka_fhir_adapter.services.fhir_patient import *

@dataclass
class EncounterResource:
    id: None 
    data_atualizacao_tasy: None 
    nr_atendimento: Optional[str]
    prontuario: Optional[str]
    cpf_paciente: Optional[str]
    cnpj_estabelecimento: Optional[str]
    nome_setor_atendimento: Optional[str]
    cpf_medico: Optional[str]
    tipo_atendimento: Optional[str]
    dt_entrada: Optional[str]
    dt_alta: Optional[str]
    motivo_alta: Optional[str]
    status_atendimento: Optional[str]


    @classmethod
    def from_dict(cls, message : dict):
        return cls(
            id=None,
            data_atualizacao_tasy=None,
            nr_atendimento = message.get('NR_ATENDIMENTO',None),
            prontuario = message.get('PRONTUARIO',None) ,
            cpf_paciente = message.get('CPF_PACIENTE',None),
            cnpj_estabelecimento = message.get('CNPJ_ESTABELECIMENTO',None),
            nome_setor_atendimento=message.get('NOME_SETOR_ATENDIMENTO',None),
            cpf_medico = message.get('CPF_MEDICO',None),
            tipo_atendimento = message.get('TIPO_ATENDIMENTO',None),
            dt_entrada = message.get('DT_ENTRADA',None),
            dt_alta = message.get('DT_ALTA',None),
            motivo_alta = message.get('DS_MOTIVO_ALTA',None),
            status_atendimento = message.get('STATUS_ATENDIMENTO',None)
        )
    
    async def to_fhir(self):
        if not self.tipo_atendimento:
            raise AttributeError("tipo_atendimento is required | Encounter.class is required")

        tipo_atendimento_mapping = {
            "Internado": "IMP",    # Internado -> Inpatient Encounter
            "Pronto socorro": "EMER",   # Pronto Socorro -> Emergency Encounter
            "Atendimento domiciliar": "HH",     # Atendimento Domiciliar -> Home Health Encounter
            "Externo": "FLD",    # Externo -> Field Encounter
            "Ambulatorial": "AMB"     # Ambulatorial -> Ambulatory Encounter
        }

        codigo_fhir_class = tipo_atendimento_mapping.get(self.tipo_atendimento)

        if not codigo_fhir_class:
            raise ValueError(f"Tipo de atendimento inválido: {self.tipo_atendimento}")

        # required element
        encounter_class = Coding(
            system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
            code=codigo_fhir_class
        )
        
        if not self.status_atendimento:
            raise AttributeError("status_atendimento is required | Encounter.status is required")
            
        status_atendimento_mapping = {
            "Atendido": "finished",      # Atendido -> Finished
            "Em espera": "planned",       # Em espera -> Planned
            "Em consulta": "in-progress"    # Em consulta -> In Progress
        }
        
        # required element
        codigo_fhir_status = status_atendimento_mapping.get(self.status_atendimento)
        
        if not codigo_fhir_status:
            raise ValueError(f"Status de atendimento inválido: {self.status_atendimento}")       


        encounter = Encounter(
            meta = Meta(profile=["https://fhir.omnisaude.co/r4/core/StructureDefinition/encounter"]),
            class_fhir=encounter_class,
            status=codigo_fhir_status
            )

        if self.cnpj_estabelecimento:
            organization_id = await get_organization_id_by_cnpj(self.cnpj_estabelecimento)
            
            if organization_id:
                encounter.serviceProvider = Reference(
                    reference=f"Organization/{organization_id}"
                )

        if self.nome_setor_atendimento:
            id_location = await get_location_id_by_name_and_organization_id(self.nome_setor_atendimento, organization_id)
            
            if id_location:
                encounter.location = Reference(
                    reference=f"Location/{id_location}"
                )

        if self.dt_entrada:
            encounter_data_inicio = epoch_timestamp_to_iso_string(int(self.dt_entrada))

        if self.dt_alta:
            encounter_data_fim = epoch_timestamp_to_iso_string(int(self.dt_alta))

        if encounter_data_inicio or encounter_data_fim:
            encounter.period = Period(
                start= encounter_data_inicio,
                end= encounter_data_fim
            )

        patient_reference = None
        
        if self.cpf_paciente:
            patient_id = await get_patient_id_by_cpf(self.cpf_paciente)
            
            if patient_id:
                patient_reference = Reference(
                    reference=f"Patient/{patient_id}" 
                )
                
        if self.prontuario and not patient_reference:
            patient_id = await get_patient_id_by_prontuario_amh(self.prontuario)
            
            if patient_id:
                patient_reference = Reference(
                    reference=f"Patient/{patient_id}" 
                )
                
        encounter.subject = patient_reference
    
        return encounter
