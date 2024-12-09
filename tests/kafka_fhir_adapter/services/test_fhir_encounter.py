import pytest

from kafka_fhir_adapter.services.fhir_encounter import *

from fhir.resources.R4B.identifier import Identifier


async def test_get_encounter_by_identifier():
    identifier = Identifier(system="https://fhir.omnisaude.co/r4/core/sid/numero-atendimento-americas-health", value="545004")
    encounter_json = await get_encounter_by_identifier(identifier)
    assert encounter_json is not None
    assert encounter_json["id"] == "2086"


async def test_get_encounter_by_system_value():
    system="https://fhir.omnisaude.co/r4/core/sid/numero-atendimento-americas-health"
    value="545004"
    encounter_json = await get_encounter_by_system_value(system, value)
    assert encounter_json is not None
    assert encounter_json["id"] == "2086"


async def test_get_encounter_by_nr_atendimento():
    encounter_json = await get_encounter_id_by_nr_atendimento("545004")
    assert encounter_json is not None
    assert encounter_json == "2086"