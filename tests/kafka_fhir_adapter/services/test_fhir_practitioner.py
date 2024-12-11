from kafka_fhir_adapter.services.fhir_practitioner import *


async def test_get_practitioner_by_identifier():
    identifier = Identifier(system="https://fhir.omnisaude.co/r4/core/sid/cpf", value="03276299359")
    practitioner_json = await get_practitioner_by_identifier(identifier)
    assert practitioner_json is not None
    assert practitioner_json["id"] == "profissional-01"

async def test_get_practitioner_by_system_value():
    system="https://fhir.omnisaude.co/r4/core/sid/cpf"
    value="03276299359"
    practitioner_json = await get_practitioner_by_system_value(system, value)
    assert practitioner_json is not None
    assert practitioner_json["id"] == "profissional-01"

async def test_get_practitioner_by_cpf():
    practitioner_json = await get_practitioner_by_cpf("03276299359")
    assert practitioner_json is not None
    assert practitioner_json["id"] == "profissional-01"