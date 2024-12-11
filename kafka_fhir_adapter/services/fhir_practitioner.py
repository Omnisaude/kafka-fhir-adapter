import requests

from fhir.resources.R4B.identifier import Identifier

from typing import Optional

from kafka_fhir_adapter.config import FHIR_BASE_URL


FHIR_PRACTITIONER_URL = f"{FHIR_BASE_URL}/Practitioner"
TIMEOUT_DEFAULT = 10

CPF_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/cpf"

async def get_practitioner_by_identifier(identifier: Identifier) -> Optional[str]:
    params = {
        'identifier': f'{identifier.system}|{identifier.value}'
    }

    try:
        response = requests.get(FHIR_PRACTITIONER_URL, params=params, timeout=TIMEOUT_DEFAULT)

        if response.status_code == 200:
            data = response.json()
            
            if "entry" in data:
                return data["entry"][0]["resource"]
        return None
    
    except requests.exceptions.Timeout:
        print(f"Timeout ao acessar {FHIR_PRACTITIONER_URL}")
    except requests.exceptions.RequestException:
        print(f"Erro ao acessar {FHIR_PRACTITIONER_URL}")
    except Exception as e:
        print(f"Erro inesperado ao acessar {FHIR_PRACTITIONER_URL}: {e}")
    
    return None

async def get_practitioner_by_system_value(system: str, value: str) -> Optional[str]:
    if  system and value:
        identifier = Identifier(system=system, value=value)
        return await get_practitioner_by_identifier(identifier)
    
    return None

async def get_practitioner_by_cpf(cpf: str) -> Optional[str]:
    return await get_practitioner_by_system_value(CPF_SYSTEM, cpf)

async def get_practitioner_id_by_cpf(cpf: str) -> Optional[str]:
    practitioner = await get_practitioner_by_cpf(cpf)
    if practitioner:
        return practitioner["id"]
    return None

