import uuid
from dataclasses import dataclass, field

from fhir.resources.R4B.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhir.resources.R4B.quantity import Quantity
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.observation import Observation, ObservationComponent
from fhir.resources.R4B.meta import Meta

from kafka_fhir_adapter.services.fhir_encounter import get_encounter_id_by_nr_atendimento
from kafka_fhir_adapter.services.fhir_patient import *


@dataclass
class SinalVital:
    id: Optional[str]
    numero_atendimento: Optional[str]
    
    cpf_paciente: Optional[str]
    numero_prontuario_amh: Optional[str]
    
    cpf_profissional: Optional[str]
    
    frequencia_respiratoria_valor: Optional[str]
    frequencia_cardiaca_valor: Optional[str]
    pressao_arterial_sistolica_valor: Optional[str]
    pressao_arterial_media_valor: Optional[str]
    pressao_arterial_diastolica_valor: Optional[str]
    temperatura_valor: Optional[str]
    saturacao_oxigenio_valor: Optional[str]
    
    data_hora_sinal_vital: Optional[str]
    data_hora_liberacao: Optional[str]

    meta: Meta = field(default_factory=lambda:Meta(profile=["https://fhir.omnisaude.co/r4/core/StructureDefinition/observacao"]))
    category: CodeableConcept = field(default_factory=lambda: CodeableConcept(
        coding=[
            Coding(
                code="vital-signs",
                system="http://terminology.hl7.org/CodeSystem/observation-category"
            )
        ]
    ))
    status: str = "final"

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id=message.get('NR_SEQUENCIA', None),
            numero_atendimento=message.get('NR_ATENDIMENTO', None),
            cpf_paciente=message.get('CPF_PACIENTE', None),
            numero_prontuario_amh=message.get('NR_PRONTUARIO_AMH', None),
            cpf_profissional=message.get('CPF_PROFISSIONAL', None),
            frequencia_respiratoria_valor=message.get('FREQUENCIA_RESPIRATORIA_VALOR', None),
            frequencia_cardiaca_valor=message.get('FREQUENCIA_CARDIACA_VALOR', None),
            pressao_arterial_sistolica_valor=message.get('PRESSAO_ARTERIAL_SISTOLICA_VALOR', None),
            pressao_arterial_diastolica_valor=message.get('PRESSAO_ARTERIAL_DIASTOLICA_VALOR', None),
            pressao_arterial_media_valor=message.get('PRESSAO_ARTERIAL_MEDIA_VALOR', None),
            temperatura_valor=message.get('TEMPERATURA_VALOR', None),
            saturacao_oxigenio_valor=message.get('SATURACAO_OXIGENIO_VALOR', None),
            data_hora_sinal_vital=message.get('DATA_HORA_SINAL_VITAL', None),
            data_hora_liberacao=message.get('DATA_HORA_LIBERACAO', None)
        )

    def is_valid(self) -> bool:
        if not self.cpf_paciente and not self.numero_prontuario_amh:
            return False

        if not any([
                self.frequencia_respiratoria_valor,
                self.frequencia_cardiaca_valor,
                self.pressao_arterial_sistolica_valor,
                self.pressao_arterial_diastolica_valor,
                self.pressao_arterial_media_valor,
                self.temperatura_valor,
                self.saturacao_oxigenio_valor
                ]):
            return False

        if not self.data_hora_sinal_vital or not self.data_hora_liberacao or not self.numero_atendimento:
            return False

        return True

    async def vital_signs_base(self, observation_code: str) -> Optional[Observation]:
        vital_sign_base = Observation(
            meta=self.meta,
            category=[self.category],
            code=CodeableConcept(
                coding=[
                    Coding(
                        code=observation_code,
                        system="http://loinc.org"
                    )
                ]
            ),
            status=self.status
        )

        patient_id = await get_patient_id(cpf=self.cpf_paciente, prontuario_amh=self.numero_prontuario_amh)

        if not patient_id:
            return None

        vital_sign_base.subject = Reference(
            reference="Patient/" + patient_id
        )

        encounter_id = await get_encounter_id_by_nr_atendimento(self.numero_atendimento)

        if not encounter_id:
            return None

        vital_sign_base.encounter = Reference(
            reference="Encounter/" + encounter_id
        )

        vital_sign_base.effectiveDateTime = self.data_hora_sinal_vital

        vital_sign_base.issued = self.data_hora_liberacao

        return vital_sign_base

    async def to_fhir(self) -> Bundle | None:
        if not self.is_valid():
            return None

        vital_signs_painel_code = "85353-1"

        # Atributo: [observation_code, unit]
        fhir_mapping = {
            "frequencia_respiratoria_valor": ["9279-1", "/min"],
            "frequencia_cardiaca_valor": ["8867-4", "/min"],
            "temperatura_valor": ["8310-5", "Cel"],
            "saturacao_oxigenio_valor": ["2708-6", "%"]
        }

        vital_signs_resources = []
        for attribute, [observation_code, unit] in fhir_mapping.items():
            value = getattr(self, attribute)
            if value:
                vital_signs_resources.append(await self.create_sinal_vital(observation_code, value, unit))

        blood_pressure_painel = await self.create_blood_pressure_painel()
        if blood_pressure_painel:
            vital_signs_resources.append(blood_pressure_painel)


        vital_signs_painel = await self.vital_signs_base(vital_signs_painel_code)
        vital_signs_painel.hasMember = []

        bundle_trasaction = Bundle(type="transaction", entry=[])

        for vital_sign in vital_signs_resources:
            full_url = "urn:uuid:" + str(uuid.uuid4())

            vital_signs_painel.hasMember.append(Reference(
                reference=full_url
            ))

            entry = BundleEntry(
                fullUrl=full_url,
                resource=vital_sign,
                request=BundleEntryRequest(
                    method="POST",
                    url="Observation"
                )
            )

            bundle_trasaction.entry.append(entry)

        bundle_trasaction.entry.append(
            BundleEntry(
                fullUrl="urn:uuid:" + str(uuid.uuid4()),
                resource=vital_signs_painel,
                request=BundleEntryRequest(
                    method="POST",
                    url="Observation"
                )
            )
        )

        return bundle_trasaction

    async def create_sinal_vital(self, observation_code: str, value: str, unit_code: str) -> Observation:
        vital_sign = await self.vital_signs_base(observation_code)

        vital_sign.valueQuantity = Quantity(
            value=value,
            unit=unit_code,
            code=unit_code,
            system="http://unitsofmeasure.org"
        )

        return vital_sign

    async def create_blood_pressure_painel(self) -> Optional[Observation]:
        blood_pressure_painel_code = "85354-9"

        # Atributo: [observation_code, unit]
        fhir_mapping = {
            "pressao_arterial_sistolica_valor": ["8480-6", "mm[Hg]"],
            "pressao_arterial_diastolica_valor": ["8462-4", "mm[Hg]"],
            "pressao_arterial_media_valor": ["8478-0", "mm[Hg]"]
        }

        blood_pressure_painel = await self.vital_signs_base(blood_pressure_painel_code)

        component = []

        for attribute, [observation_code, unit] in fhir_mapping.items():
            value = getattr(self, attribute)
            # TODO: Precisa converter o valor?
            if value:
                component.append(ObservationComponent(
                    code= CodeableConcept(
                        coding=[
                            Coding(
                                code=observation_code,
                                system="http://loinc.org"
                            )
                        ]
                    ),
                    valueQuantity= Quantity(
                        value=value,
                        unit=unit,
                        code=unit,
                        system="http://unitsofmeasure.org"
                    )
                ))

        if not component:
            return None

        blood_pressure_painel.component = component

        return blood_pressure_painel