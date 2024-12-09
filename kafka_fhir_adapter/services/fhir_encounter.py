import requests
from kafka_fhir_adapter.config import *

from fhir.resources.R4B.identifier import Identifier
from typing import Optional


FHIR_ENCOUNTER_URL = f"{FHIR_BASE_URL}/Encounter"
TIMEOUT_DEFAULT = 10

NR_ATENDIMENTO_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/numero-atendimento-americas-health"


async def get_encounter_by_identifier(identifier: Identifier) -> Optional[str]:
    params = {
        'identifier': f'{identifier.system}|{identifier.value}'
    }

    try:
        response = requests.get(FHIR_ENCOUNTER_URL, params=params, timeout=TIMEOUT_DEFAULT)

        if response.status_code == 200:
            data = response.json()

            if "entry" in data:
                return data["entry"][0]["resource"]
        return None

    except requests.exceptions.Timeout:
        print(f"Timeout ao acessar {FHIR_ENCOUNTER_URL}")
    except requests.exceptions.RequestException:
        print(f"Erro ao acessar {FHIR_ENCOUNTER_URL}")
    except Exception as e:
        print(f"Erro inesperado ao acessar {FHIR_ENCOUNTER_URL}: {e}")

    return None

async def get_encounter_by_system_value(system: str, value: str) -> Optional[str]:
    if system and value:
        identifier = Identifier(system=system, value=value)
        return await get_encounter_by_identifier(identifier)

    return None

async def get_encounter_by_nr_atendimento(nr_atendimento: str):
    return await get_encounter_by_system_value(NR_ATENDIMENTO_SYSTEM, nr_atendimento)

async def get_encounter_id_by_nr_atendimento(nr_atendimento: str):
    encounter = await get_encounter_by_nr_atendimento(nr_atendimento)
    if encounter:
        return encounter['id']
    return None