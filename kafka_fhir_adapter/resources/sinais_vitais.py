import uuid
from dataclasses import dataclass, field

from fhir.resources.R4B.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhir.resources.R4B.quantity import Quantity
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.observation import Observation, ObservationComponent
from fhir.resources.R4B.meta import Meta

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
        # TODO: tem mais critérios id, data_liberacao, cpf_profissional, nr_atendimento ...?
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

        if not self.data_hora_sinal_vital:
            return False

        return True

    def vital_signs_base(self, observation_code: str, patient_id: str) -> Observation:
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

        vital_sign_base.subject = Reference(
            reference="Patient/" + patient_id
        )

        vital_sign_base.effectiveDateTime = self.data_hora_sinal_vital.replace(" ", "T") + "-03:00"

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

        patient_id = await get_patient_id(cpf=self.cpf_paciente, prontuario_amh=self.numero_prontuario_amh)

        if not patient_id:
            return None

        vital_signs_resources = []
        for attribute, [observation_code, unit] in fhir_mapping.items():
            value = getattr(self, attribute)
            if value:
                vital_signs_resources.append(self.create_sinal_vital(patient_id, observation_code, value, unit))

        blood_pressure_painel = self.create_blood_pressure_painel(patient_id)
        if blood_pressure_painel:
            vital_signs_resources.append(blood_pressure_painel)


        vital_signs_painel = self.vital_signs_base(vital_signs_painel_code, patient_id)
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

    def create_sinal_vital(self, patient_id: str, observation_code: str, value: str, unit_code: str) -> Observation:
        vital_sign = self.vital_signs_base(observation_code, patient_id)

        vital_sign.valueQuantity = Quantity(
            value=value,
            unit=unit_code,
            code=unit_code,
            system="http://unitsofmeasure.org"
        )

        return vital_sign

    def create_blood_pressure_painel(self, patient_id: str) -> Optional[Observation]:
        blood_pressure_painel_code = "85354-9"

        # Atributo: [observation_code, unit]
        fhir_mapping = {
            "pressao_arterial_sistolica_valor": ["8480-6", "mm[Hg]"],
            "pressao_arterial_diastolica_valor": ["8462-4", "mm[Hg]"],
            "pressao_arterial_media_valor": ["8478-0", "mm[Hg]"]
        }

        blood_pressure_painel = self.vital_signs_base(blood_pressure_painel_code, patient_id)

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