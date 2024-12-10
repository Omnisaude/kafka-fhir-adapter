import json

from kafka_fhir_adapter.resources.sinais_vitais import SinalVital

complete_message_patient = '''{
  "NR_SEQUENCIA": "1",
  "NR_ATENDIMENTO": "1234567890",
  "NR_PRONTUARIO_AMH": "54321",
  "CPF_PACIENTE": "123456789",
  "CPF_PROFISSIONAL": "03276299359",
  "FREQUENCIA_RESPIRATORIA_VALOR": "13",
  "FREQUENCIA_CARDIACA_VALOR": "54",
  "PRESSAO_ARTERIAL_SISTOLICA_VALOR": "127",
  "PRESSAO_ARTERIAL_MEDIA_VALOR": "88",
  "PRESSAO_ARTERIAL_DIASTOLICA_VALOR": "68",
  "TEMPERATURA_VALOR": "37",
  "SATURACAO_OXIGENIO_VALOR": "99",
  "DATA_HORA_SINAL_VITAL": "2024-06-25 21:30:47.000",
  "DATA_HORA_LIBERACAO": "2024-06-25 21:31:28.000"
}'''


async def test_create_vital_signs():
  message = json.loads(complete_message_patient)

  vital_sign_resource = SinalVital.from_dict(message)

  bundle = await vital_sign_resource.to_fhir()

  assert bundle.entry[0].resource.code.coding[0].code == "9279-1"
  assert bundle.entry[1].resource.code.coding[0].code == "8867-4"
  assert bundle.entry[2].resource.code.coding[0].code == "8310-5"
  assert bundle.entry[3].resource.code.coding[0].code == "2708-6"
  assert bundle.entry[4].resource.code.coding[0].code == "85354-9"
  assert len(bundle.entry[4].resource.component) == 3
  assert bundle.entry[4].resource.component[0].code.coding[0].code == "8480-6"
  assert bundle.entry[4].resource.component[1].code.coding[0].code == "8462-4"
  assert bundle.entry[4].resource.component[2].code.coding[0].code == "8478-0"
