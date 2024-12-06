import json

from kafka_fhir_adapter.resources.encounter import EncounterResource

complete_message_patient = '''{
  "DATA_ATUALIZACAO": 1728302742000,
  "NR_ATENDIMENTO": 1,
  "PRONTUARIO": 229759,
  "CPF_PACIENTE": 123456789,
  "CNPJ_ESTABELECIMENTO": "03771319000109",
  "NOME_SETOR_ATENDIMENTO": "Gasômetro",
  "CPF_MEDICO": null,
  "TIPO_ATENDIMENTO": "Internado",
  "DT_ENTRADA": "1733011200",
  "DT_ALTA": "1733011200",
  "DS_MOTIVO_ALTA": null,
  "STATUS_ATENDIMENTO": "Atendido"
}'''


async def test_create_encounter_complete():
  message = json.loads(complete_message_patient)

  encounter_resource = EncounterResource.from_dict(message)
  encounter = await encounter_resource.to_fhir()
  assert encounter.status == "finished"
  assert encounter.subject.reference == "Patient/paciente-01"
  assert encounter.identifier[0].value == "1"
  