import json

from kafka_fhir_adapter.resources.patient import is_address_empty, PatientResource

complete_message_patient = '''{
  "CODIGO_PESSOA_FISICA": "1231231",
  "DATA_ATUALIZACAO": 1728302742000,
  "NOME_PAI": "Paiteste da Silva",
  "NOME_MAE": "Mãeteste da Silva",
  "CODIGO_NACIONALIDADE": "10",
  "CODIGO_RACA": "01",
  "CODIGO_ETNIA": null,
  "PRONTUARIO": "123234",
  "CPF": "123234",
  "CARTAO_NACIONAL_SAUDE": null,
  "NOME_PACIENTE": "Testevaldo da Silva",
  "CODIGO_SEXO": "FEMALE",
  "DATA_NASCIMENTO": "1957-08-12",
  "CODIGO_TIPO_LOGRADOURO": null,
  "LOGRADOURO": "Rua da Silva ",
  "NUMERO": "123",
  "COMPLEMENTO": null,
  "BAIRRO": "Centro ",
  "CODIGO_IBGE_CIDADE": "171820",
  "CODIGO_IBGE_ESTADO": "17",
  "CODIGO_PAIS": "BRA",
  "CEP": "77500000",
  "ENDERECO_COMPLETO": "Rua da Silva, 123 , Centro , 77500000, Porto Nacional - TO, Brasil",
  "TELEFONE": "+55 62 902750388"
}'''


no_address_message_patient = '''{
  "CODIGO_PESSOA_FISICA": "1231231",
  "DATA_ATUALIZACAO": 1728302742000,
  "NOME_PAI": "Paiteste da Silva",
  "NOME_MAE": "Mãeteste da Silva",
  "CODIGO_NACIONALIDADE": "10",
  "CODIGO_RACA": "01",
  "CODIGO_ETNIA": "001",
  "PRONTUARIO": "123234",
  "CPF": "123234",
  "CARTAO_NACIONAL_SAUDE": null,
  "NOME_PACIENTE": "Testevaldo da Silva",
  "CODIGO_SEXO": "FEMALE",
  "DATA_NASCIMENTO": "1957-08-12",
  "CODIGO_TIPO_LOGRADOURO": null,
  "LOGRADOURO": null,
  "NUMERO": null,
  "COMPLEMENTO": null,
  "BAIRRO": null,
  "CODIGO_IBGE_CIDADE": null,
  "CODIGO_IBGE_ESTADO": null,
  "CODIGO_PAIS": null,
  "CEP": null,
  "ENDERECO_COMPLETO": null,
  "TELEFONE": null
}'''


  
  
def test_create_patient_complete():
  message = json.loads(complete_message_patient)

  patient_resource = PatientResource.from_dict(message)
  patient = patient_resource.to_fhir()

  assert patient.name[0].text == "Testevaldo da Silva"
  assert patient.birthDate.strftime("%Y-%m-%d") == "1957-08-12"
  assert patient.gender == "female"
  assert patient.identifier[0].system == "https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health"
  assert patient.identifier[0].value == "123234"
  assert patient.identifier[1].system == "https://fhir.omnisaude.co/r4/core/sid/cpf"
  assert patient.identifier[1].value == "123234"
  assert patient.extension[0].url == "http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName"
  assert patient.extension[0].valueString == "Mãeteste da Silva"
  assert patient.extension[1].url == "https://fhir.omnisaude.co/r4/core/StructureDefinition/nome-pai-paciente"
  assert patient.extension[1].valueString == "Paiteste da Silva"
  assert patient.extension[2].url == "http://hl7.org/fhir/StructureDefinition/patient-nationality"
  assert patient.extension[2].extension[0].valueCodeableConcept.coding[0].system == "http://www.saude.gov.br/fhir/r4/CodeSystem/BRPais"
  assert patient.extension[2].extension[0].valueCodeableConcept.coding[0].code == "10"
  assert patient.extension[3].url == "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRRacaCorEtnia-1.0"
  assert patient.extension[3].extension[0].valueCodeableConcept.coding[0].system == "http://www.saude.gov.br/fhir/r4/CodeSystem/BRRacaCor"
  assert patient.extension[3].extension[0].valueCodeableConcept.coding[0].code == "01"
  assert patient.address[0].country == "BRA"
  assert patient.address[0].state == "17"
  assert patient.address[0].city == "171820"
  assert patient.address[0].postalCode == "77500000"
  assert patient.address[0].text == "Rua da Silva, 123 , Centro , 77500000, Porto Nacional - TO, Brasil"
  assert patient.address[0].line[0] == "Rua da Silva "
  assert patient.address[0].line[1] == "123"
  assert patient.address[0].line[2] == "Centro "
  assert patient.address[0].line__ext[0].id == "logradouro"
  assert patient.address[0].line__ext[1].id == "numero"
  assert patient.address[0].line__ext[2].id == "bairro"

def test_is_address_empty_true():
  message = json.loads(no_address_message_patient)
  
  patient_resource = PatientResource.from_dict(message)
  
  endereco = patient_resource.create_address()
  
  assert is_address_empty(endereco)

def test_is_address_empty_false():
  message = json.loads(complete_message_patient)
  
  patient_resource = PatientResource.from_dict(message)

  endereco = patient_resource.create_address()
  
  assert not is_address_empty(endereco)

def test_create_address_complete():
  message = json.loads(complete_message_patient)
  
  patient_resource = PatientResource.from_dict(message)
  
  endereco = patient_resource.create_address()
  
  assert endereco.country == "BRA"
  assert endereco.state == "17"
  assert endereco.city == "171820"
  assert endereco.postalCode == "77500000"
  assert endereco.text == "Rua da Silva, 123 , Centro , 77500000, Porto Nacional - TO, Brasil"
  assert endereco.line[0] == "Rua da Silva "
  assert endereco.line[1] == "123"
  assert endereco.line[2] == "Centro "        
  assert endereco.line__ext[0].id == "logradouro"
  assert endereco.line__ext[1].id == "numero"
  assert endereco.line__ext[2].id == "bairro"

def test_create_address_empty():
  message = json.loads(no_address_message_patient)

  patient_resource = PatientResource.from_dict(message)
  
  endereco = patient_resource.create_address()
  
  assert endereco.country is None
  assert endereco.state is None
  assert endereco.city is None
  assert endereco.postalCode is None
  assert endereco.text is None
  assert endereco.line is None
  assert endereco.line__ext is None
