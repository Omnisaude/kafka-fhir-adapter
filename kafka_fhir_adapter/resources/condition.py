from dataclasses import dataclass
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.condition import Condition
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.period import Period
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.reference import Reference
from kafka_fhir_adapter.services.fhir_patient import *
from typing import Optional
from kafka_fhir_adapter.services.fhir_encounter import *


@dataclass
class ConditionResource:
    id: None
    data_atulizacao_tasy:None
    code: Optional[str]
    encounter_code: Optional[str]
    patient_reference_prontuario: Optional[str]
    patient_reference_cpf: Optional[str]
    name: Optional[str]
    category: Optional[str]
    type: Optional[str]
    clinical_status: Optional[str]
    date: Optional[str]
    practitioner_cpf: Optional[str]

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id= None,
            data_atulizacao_tasy= None,
            code= message.get("CONDITION_CODE",None),
            encounter_code= message.get("CONDITION_ENCOUNTER_CODE",None),
            patient_reference_prontuario= message.get("CONDITION_PATIENT_PRONTUARIO",None),
            patient_reference_cpf= message.get("CONDITION_PATIENT_CPF",None),
            name= message.get("CONDITION_NAME",None),
            category= message.get("CONDITION_CATEGORY",None),
            type= message.get("CONDITION_TYPE",None),
            clinical_status= message.get("CONDITION_CLINICAL_STATUS",None),
            date= message.get("CONDITION_DATE",None),
            practitioner_cpf= message.get("CPF_MEDICO",None),
        )

    async def to_fhir(self) -> Condition:

        patient_reference = None
        patient_id = await get_patient_id(cpf=self.patient_reference_cpf, prontuario_amh=self.patient_reference_prontuario)

        if patient_id:
            patient_reference = Reference(
                reference=f"Patient/{patient_id}"
            )

        coding_clinical_status = Coding(
            system="http://terminology.hl7.org/CodeSystem/condition-clinical",
            code=self.clinical_status.lower()
        )
        codeable_concept_clinical_status = CodeableConcept(coding=[coding_clinical_status])


        coding_code = Coding(
            system="http://hl7.org/fhir/sid/icd-10",
            code=self.code,
            display=self.name,
        )
        codeable_concept_code = CodeableConcept(coding=[coding_code])

        condition = Condition(
            code = codeable_concept_code,
            clinicalStatus = codeable_concept_clinical_status,
            meta = Meta(profile=["https://fhir.omnisaude.co/r4/core/StructureDefinition/condicao"]),
            subject = patient_reference
        )

        verification_status_mapping = {
            "Preliminar": "provisional",
            "Definitivo": "confirmed"
        }

        coding_verification_status = verification_status_mapping.get(self.type)

        if coding_verification_status:
            coding_clinical_status_cc = Coding(
                system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
                code=coding_verification_status
            )
            codeable_concept_clinical_status = CodeableConcept(coding=[coding_clinical_status_cc])
            condition.verificationStatus = codeable_concept_clinical_status


        if self.date:
            condition.recordedDate = self.date

        if self.encounter_code:
            encounter_id = await get_encounter_id_by_nr_atendimento(self.encounter_code)

            if encounter_id:
                encounter_reference = Reference(
                    reference = f"Encounter/{encounter_id}"
                )
                condition.encounter = encounter_reference

        return condition