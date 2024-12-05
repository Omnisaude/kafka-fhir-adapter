import json

from kafka_fhir_adapter.resources.encounter import EncounterResource

complete_message_patient = '''{
  "DATA_ATUALIZACAO": 1728302742000,
  "NR_ATENDIMENTO": 1,
  "PRONTUARIO": 229759,
  "CPF_PACIENTE": null,
  "CNPJ_ESTABELECIMENTO": 03771319000109,
  "NOME_SETOR_ATENDIMENTO":"Gasômetro",
  "CPF_MEDICO":null,
  "TIPO_ATENDIMENTO":"Internado",
  "DT_ENTRADA":"2024-12-01",
  "DT_ALTA":"2024-12-03",
  "DS_MOTIVO_ALTA":null,
  "STATUS_ATENDIMENTO":"Atendido",
}'''


def test_create_encounter_complete():
  message = json.loads(complete_message_patient)

  encounter_resource = EncounterResource.from_dict(message)
  encounter = encounter_resource.to_fhir()
  assert encounter.status == "Atendido"