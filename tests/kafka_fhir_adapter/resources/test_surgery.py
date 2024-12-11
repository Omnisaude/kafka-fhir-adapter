import json
from kafka_fhir_adapter.resources.surgery import SurgeryResource
import pytest

complete_message_surgery = '''{
    "SURGERY_CODE":"24467",
    "SURGERY_PATIENT_PRONTUARIO":"54321",
    "SURGERY_PATIENT_CPF":"123456789",
    "SURGERY_ENCOUNTER_CODE":"1234567890",
    "SURGERY_PROCEDURE_CODE":"30601185",
    "SURGERY_NAME":"Toracotomia Exploradora (Excluídos Os Procedimentos Intratorácicos)",
    "SURGERY_START_DATE":"2023-06-27",
    "SURGERY_END_DATE":"2023-06-27",
    "SURGERY_STATUS":"Realizada",
    "SURGERY_TYPE":null,
    "SURGERY_LOCATION":"177",
    "SURGERY_LOCATION_NAME":"Escritório Corporativo Omnisaude",
    "SURGERY_ORGANIZATION_CNPJ":"14021734000161"
    }'''


async def test_create_surgery_complete():
  message = json.loads(complete_message_surgery)

  surgery_resource = SurgeryResource.from_dict(message)
  surgery = await surgery_resource.to_fhir()
  assert surgery.subject.reference == 'Patient/paciente-01'
  assert surgery.status == 'completed'
  assert surgery.encounter.reference == 'Encounter/encontro-01'
  assert surgery.code.coding[0].code == '30601185'
  assert surgery.code.coding[0].display == 'Toracotomia Exploradora (Excluídos Os Procedimentos Intratorácicos)'
  assert surgery.location.reference == 'Location/local-02'
  assert surgery.performedPeriod.start.strftime("%Y-%m-%d") == "2023-06-27"
  assert surgery.performedPeriod.end.strftime("%Y-%m-%d") == "2023-06-27"