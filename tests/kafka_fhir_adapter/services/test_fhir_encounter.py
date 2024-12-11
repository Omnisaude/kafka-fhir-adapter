from kafka_fhir_adapter.services.fhir_encounter import *

from fhir.resources.R4B.identifier import Identifier


async def test_get_encounter_by_identifier():
    identifier = Identifier(system="https://fhir.omnisaude.co/r4/core/sid/numero-atendimento-americas-health", value="1234567890")
    encounter_json = await get_encounter_by_identifier(identifier)
    assert encounter_json is not None
    assert encounter_json["id"] == "encontro-01"

async def test_get_encounter_by_system_value():
    system="https://fhir.omnisaude.co/r4/core/sid/numero-atendimento-americas-health"
    value="1234567890"
    encounter_json = await get_encounter_by_system_value(system, value)
    assert encounter_json is not None
    assert encounter_json["id"] == "encontro-01"

async def test_get_encounter_by_nr_atendimento():
    encounter_id = await get_encounter_id_by_nr_atendimento("1234567890")
    assert encounter_id is not None
    assert encounter_id == "encontro-01"