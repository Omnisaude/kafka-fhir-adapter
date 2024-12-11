import json
from kafka_fhir_adapter.resources.surgery import SurgeryResource
import pytest

complete_message_surgery = '''{
    "SURGERY_CODE":"24467",
    "SURGERY_PATIENT_PRONTUARIO":"199115",
    "SURGERY_PATIENT_CPF":"52791220178",
    "SURGERY_ENCOUNTER_CODE":"544236",
    "SURGERY_PROCEDURE_CODE":"30601185",
    "SURGERY_NAME":"Toracotomia Exploradora (Excluídos Os Procedimentos Intratorácicos)",
    "SURGERY_START_DATE":"2023-06-27",
    "SURGERY_END_DATE":"2023-06-27",
    "SURGERY_STATUS":"Realizada",
    "SURGERY_TYPE":null,
    "SURGERY_LOCATION":"177",
    "SURGERY_LOCATION_NAME":"Clínica Cirúrgica - HIOP",
    "SURGERY_ORGANIZATION_CNPJ":"07169771000156"
    }'''


async def test_create_surgery_complete():
  message = json.loads(complete_message_surgery)

  surgery_resource = SurgeryResource.from_dict(message)
  surgery = await surgery_resource.to_fhir()
  assert surgery.subject.reference == 'Patient/761'
  assert surgery.status == 'completed'
  #assert surgery.encounter.reference == 'Encounter/2081'
  assert surgery.code.coding[0].code == '30601185'
  assert surgery.code.coding[0].display == 'Toracotomia Exploradora (Excluídos Os Procedimentos Intratorácicos)'
  assert surgery.location.reference == 'Location/1139'
  assert surgery.performedPeriod.start.strftime("%Y-%m-%d") == "2023-06-27"
  assert surgery.performedPeriod.end.strftime("%Y-%m-%d") == "2023-06-27"