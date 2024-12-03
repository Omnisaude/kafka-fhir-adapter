import unittest
import json
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.fhirprimitiveextension import FHIRPrimitiveExtension

from src.resources.patient import create_address, is_address_empty, init_patient

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


class TestPaciente(unittest.TestCase):    
  
  def test_create_patient_complete(self):
    message = json.loads(complete_message_patient)
    
    patient = init_patient(message)
    
    self.assertEqual(patient.name[0].text, "Testevaldo da Silva")
    self.assertEqual(patient.birthDate.strftime("%Y-%m-%d"), "1957-08-12")
    self.assertEqual(patient.gender, "female")
    self.assertEqual(patient.identifier[0].system, "https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health")
    self.assertEqual(patient.identifier[0].value, "123234")
    self.assertEqual(patient.identifier[1].system, "https://fhir.omnisaude.co/r4/core/sid/cpf")
    self.assertEqual(patient.identifier[1].value, "123234")
    self.assertEqual(patient.extension[0].url, "http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName")
    self.assertEqual(patient.extension[0].valueString, "Mãeteste da Silva")
    self.assertEqual(patient.extension[1].url, "https://fhir.omnisaude.co/r4/core/StructureDefinition/nome-pai-paciente")
    self.assertEqual(patient.extension[1].valueString, "Paiteste da Silva")
    self.assertEqual(patient.extension[2].url, "http://hl7.org/fhir/StructureDefinition/patient-nationality")
    self.assertEqual(patient.extension[2].extension[0].valueCodeableConcept.coding[0].system, "http://www.saude.gov.br/fhir/r4/CodeSystem/BRPais")
    self.assertEqual(patient.extension[2].extension[0].valueCodeableConcept.coding[0].code, "10")
    self.assertEqual(patient.extension[3].url, "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRRacaCorEtnia-1.0")
    self.assertEqual(patient.extension[3].extension[0].valueCodeableConcept.coding[0].system, "http://www.saude.gov.br/fhir/r4/CodeSystem/BRRacaCor")
    self.assertEqual(patient.extension[3].extension[0].valueCodeableConcept.coding[0].code, "01")
    self.assertEqual(patient.address[0].country, "BRA")
    self.assertEqual(patient.address[0].state, "17")
    self.assertEqual(patient.address[0].city, "171820")
    self.assertEqual(patient.address[0].postalCode, "77500000")
    self.assertEqual(patient.address[0].text, "Rua da Silva, 123 , Centro , 77500000, Porto Nacional - TO, Brasil")
    self.assertEqual(patient.address[0].line[0], "Rua da Silva ")
    self.assertEqual(patient.address[0].line[1], "123")
    self.assertEqual(patient.address[0].line[2], "Centro ")
    self.assertEqual(patient.address[0].line__ext[0].id, "logradouro")
    self.assertEqual(patient.address[0].line__ext[1].id, "numero")
    self.assertEqual(patient.address[0].line__ext[2].id, "bairro")
  
  def test_is_address_empty_true(self):
      message = json.loads(no_address_message_patient)
      
      endereco = create_address(message)
      
      self.assertTrue(is_address_empty(endereco))

  def test_is_address_empty_false(self):
      message = json.loads(complete_message_patient)
      
      endereco = create_address(message)
      
      self.assertFalse(is_address_empty(endereco))

  def test_create_address_complete(self):
      message = json.loads(complete_message_patient)
      
      endereco = create_address(message)
      
      self.assertEqual(endereco.country, "BRA")
      self.assertEqual(endereco.state, "17")
      self.assertEqual(endereco.city, "171820")
      self.assertEqual(endereco.postalCode, "77500000")
      self.assertEqual(endereco.text, "Rua da Silva, 123 , Centro , 77500000, Porto Nacional - TO, Brasil")
      self.assertEqual(endereco.line[0], "Rua da Silva ")
      self.assertEqual(endereco.line[1], "123")
      self.assertEqual(endereco.line[2], "Centro ")        
      self.assertEqual(endereco.line__ext[0].id, "logradouro")
      self.assertEqual(endereco.line__ext[1].id, "numero")
      self.assertEqual(endereco.line__ext[2].id, "bairro")

  def test_create_address_empty(self):
      message = json.loads(no_address_message_patient)
      
      endereco = create_address(message)
      
      self.assertIsNone(endereco.country)
      self.assertIsNone(endereco.state)
      self.assertIsNone(endereco.city)
      self.assertIsNone(endereco.postalCode)
      self.assertIsNone(endereco.text)
      self.assertIsNone(endereco.line)
      self.assertIsNone(endereco.line__ext)

if __name__ == '__main__':
    unittest.main()