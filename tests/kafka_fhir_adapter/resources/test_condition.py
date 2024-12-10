import json
from kafka_fhir_adapter.resources.condition import ConditionResource
import pytest

complete_message_condition = '''{
    "CONDITION_CODE":"C780",
    "CONDITION_ENCOUNTER_CODE":"1234567890",
    "CONDITION_PATIENT_PRONTUARIO":"54321",
    "CONDITION_PATIENT_CPF":"123456789",
    "CONDITION_NAME":"NEOPLASIA MALIGNA SECUNDARIA DOS PULMOES",
    "CONDITION_CATEGORY":"Principal",
    "CONDITION_TYPE":"Definitivo",
    "CONDITION_CLINICAL_STATUS":"active",
    "CONDITION_DATE":"2023-06-27 11:09:36.000",
    "CPF_MEDICO":"1"
    }'''


async def test_create_condition_complete():
  message = json.loads(complete_message_condition)

  condition_resource = ConditionResource.from_dict(message)
  condition = await condition_resource.to_fhir()
  assert condition.code.coding[0].code == 'C780'
  assert condition.subject.reference == "Patient/paciente-01"
  assert condition.clinicalStatus.coding[0].code == 'active'
  assert condition.recordedDate.strftime("%Y-%m-%d") == "2023-06-27"
  assert condition.encounter.reference == "Encounter/encontro-01"
  assert condition.verificationStatus.coding[0].code == 'confirmed'
  assert condition.meta.profile[0] == "https://fhir.omnisaude.co/r4/core/StructureDefinition/condicao"