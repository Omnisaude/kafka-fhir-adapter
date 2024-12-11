import json
from kafka_fhir_adapter.resources.practitioner import PractitionerResource

complete_message_practitioner = '''{
    "NOME_PROFISSIONAL": "João da Silva",
    "CPF": "12345678900",
    "DATA_NASCIMENTO": "1985-07-23",
    "CODIGO_TIPO_LOGRADOURO": null,
    "LOGRADOURO": "Rua das Flores",
    "NUMERO": "123",
    "COMPLEMENTO": null,
    "BAIRRO": "Jardim Primavera",
    "CODIGO_IBGE_CIDADE": "1234567",
    "CODIGO_IBGE_ESTADO": "12",
    "CODIGO_PAIS": "BRA",
    "CEP": "12345678",
    "ENDERECO_COMPLETO": "Rua das Flores, 123, Apartamento 45, Jardim Primavera, 12345678, Brasil",
    "CODIGO_SEXO": "1",
    "TELEFONE": "+55 (11) 98765-4321"
  }'''


def test_create_practitioner():
  message = json.loads(complete_message_practitioner)

  practitioner_resource = PractitionerResource.from_dict(message)
  practitioner = practitioner_resource.to_fhir()
  assert practitioner.name[0].text == "João da Silva"
  assert practitioner.meta.profile[0] == "https://fhir.omnisaude.co/r4/core/StructureDefinition/profissional"
  assert practitioner.address[0].country == "BRA"
  assert practitioner.address[0].state == "12"
  assert practitioner.address[0].city == "1234567"
  assert practitioner.address[0].postalCode == "12345678"
  assert practitioner.address[0].text == "Rua das Flores, 123, Apartamento 45, Jardim Primavera, 12345678, Brasil"
  assert practitioner.address[0].line[0] == "Rua das Flores"
  assert practitioner.address[0].line[1] == "123"
  assert practitioner.address[0].line[2] == "Jardim Primavera"
  assert practitioner.address[0].line__ext[0].id == "logradouro"
  assert practitioner.address[0].line__ext[1].id == "numero"
  assert practitioner.address[0].line__ext[2].id == "bairro"
