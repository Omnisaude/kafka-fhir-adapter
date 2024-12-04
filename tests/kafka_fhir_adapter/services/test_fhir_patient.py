import pytest

from kafka_fhir_adapter.services.fhir_patient import *

from fhir.resources.R4B.identifier import Identifier

@pytest.mark.skip(reason="Teste de integração, necessita um servidor FHIR com o paciente de CPF 123456789")
def test_get_patient_by_identifier():
    identifier = Identifier(system="https://fhir.omnisaude.co/r4/core/sid/cpf", value="123456789")
    patient_json = get_patient_by_identifier(identifier)
    assert patient_json is not None
    assert patient_json["id"] == "1"
    
@pytest.mark.skip(reason="Teste de integração, necessita um servidor FHIR com o paciente de CPF 123456789")
def test_get_patient_by_system_value():
    system="https://fhir.omnisaude.co/r4/core/sid/cpf"
    value="123456789"
    patient_json = get_patient_by_system_value(system, value)
    assert patient_json is not None
    assert patient_json["id"] == "1"

@pytest.mark.skip(reason="Teste de integração, necessita um servidor FHIR com o paciente de CPF 123456789")
def test_get_patient_by_cpf():
    patient_json = get_patient_by_cpf("123456789")
    print(patient_json)
    assert patient_json is not None
    assert patient_json["id"] == "1"