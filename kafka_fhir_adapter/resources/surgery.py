from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.procedure import Procedure
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.reference import Reference
from typing import Optional
from kafka_fhir_adapter.services.fhir_patient import *
from kafka_fhir_adapter.services.fhir_encounter import *
from kafka_fhir_adapter.services.fhir_location import *
from kafka_fhir_adapter.services.fhir_organization import *
from fhir.resources.R4B.period import Period
from dataclasses import dataclass



@dataclass
class SurgeryResource:
    id: None
    data_atualizacao_tasy: None
    surgery_key: Optional[str]
    surgery_patient_prontuario: Optional[str]
    surgery_patient_cpf: Optional[str]
    surgery_encounter_code: Optional[str]
    surgery_code: Optional[str]
    surgery_name: Optional[str]
    surgery_start_date: Optional[str]
    surgery_end_date: Optional[str]
    surgery_status: Optional[str]
    surgery_type: Optional[str]
    surgery_location: Optional[str]
    surgery_location_name: Optional[str]
    surgery_organization_cnpj: Optional[str]

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id = None,
            data_atualizacao_tasy = None,
            surgery_key= message.get("SURGERY_CODE",None),
            surgery_patient_prontuario= message.get("SURGERY_PATIENT_PRONTUARIO",None),
            surgery_patient_cpf=message.get("SURGERY_PATIENT_CPF", None),
            surgery_encounter_code= message.get("SURGERY_ENCOUNTER_CODE",None),
            surgery_code= message.get("SURGERY_PROCEDURE_CODE",None),
            surgery_name= message.get("SURGERY_NAME",None),
            surgery_start_date= message.get("SURGERY_START_DATE",None),
            surgery_end_date= message.get("SURGERY_END_DATE",None),
            surgery_status= message.get("SURGERY_STATUS",None),
            surgery_type= message.get("SURGERY_TYPE",None),
            surgery_location=message.get("SURGERY_LOCATION", None),
            surgery_location_name=message.get("SURGERY_LOCATION_NAME", None),
            surgery_organization_cnpj=message.get("SURGERY_ORGANIZATION_CNPJ", None),
        )

    async def to_fhir(self):
        status_surgery_mapping = {
            "Prevista": "preparation",  # Prevista -> Preparation
            "Realizada": "completed",  # Realizada -> Completed
            "Cancelada": "not-done",  # Cancelada -> Not Done
            "Interrompida": "stopped"  # Interrompida -> Stopped
        }

        codigo_fhir_status = status_surgery_mapping.get(self.surgery_status, "unknown")

        if not codigo_fhir_status:
            raise ValueError(f"Status de procedimento inválido: {self.surgery_status}")

        patient_reference = None

        if self.surgery_patient_cpf:
            patient_id = await get_patient_id_by_cpf(self.surgery_patient_cpf)

            if patient_id:
                patient_reference = Reference(
                    reference=f"Patient/{patient_id}"
                )

        if self.surgery_patient_prontuario and not patient_reference:
            patient_id = await get_patient_id_by_prontuario_amh(self.surgery_patient_prontuario)

            if patient_id:
                patient_reference = Reference(
                    reference=f"Patient/{patient_id}"
                )

        procedure = Procedure(
            status = codigo_fhir_status,
            subject = patient_reference
        )

        if self.surgery_encounter_code:
            encounter_id = await get_encounter_id_by_nr_atendimento(self.surgery_encounter_code)

            if encounter_id:
                encounter_reference = Reference(
                    reference = f"Encounter/{encounter_id}"
                )
                procedure.encounter = encounter_reference

        if self.surgery_organization_cnpj and self.surgery_location_name:
            organization_id = await get_organization_id_by_cnpj(self.surgery_organization_cnpj)
            id_location = await get_location_id_by_name_and_organization_id(self.surgery_location_name,
                                                                            organization_id)
            if id_location:
                location_reference = Reference(
                    reference = f"Location/{id_location}"
                )
                procedure.location = location_reference

        if self.surgery_start_date or self.surgery_end_date:
            period = Period(
                start=self.surgery_start_date,
                end=self.surgery_end_date
            )
            procedure.performedPeriod = period

        if self.surgery_code:
            coding_procedure_cc = Coding(
                system="http://www.ans.gov.br/tuss",
                code=self.surgery_code,
                display= self.surgery_name
            )
            codeable_concept_procedure_code = CodeableConcept(coding=[coding_procedure_cc])
            procedure.code = codeable_concept_procedure_code

        return procedure

