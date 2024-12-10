from kafka_fhir_adapter.services.fhir_patient import *


async def test_get_patient_by_identifier():
    identifier = Identifier(system="https://fhir.omnisaude.co/r4/core/sid/cpf", value="123456789")
    patient_json = await get_patient_by_identifier(identifier)
    assert patient_json is not None
    assert patient_json["id"] == "paciente-01"

async def test_get_patient_by_system_value():
    system="https://fhir.omnisaude.co/r4/core/sid/cpf"
    value="123456789"
    patient_json = await get_patient_by_system_value(system, value)
    assert patient_json is not None
    assert patient_json["id"] == "paciente-01"

async def test_get_patient_by_cpf():
    patient_json = await get_patient_by_cpf("123456789")
    assert patient_json is not None
    assert patient_json["id"] == "paciente-01"