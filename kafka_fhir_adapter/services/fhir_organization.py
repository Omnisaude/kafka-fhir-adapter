import requests
from kafka_fhir_adapter.config import *

from fhir.resources.R4B.identifier import Identifier
from typing import Optional


FHIR_ORGANIZATION_URL = f"{FHIR_BASE_URL}/Organization"
TIMEOUT_DEFAULT = 10

CNPJ_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/cnpj"


async def get_organization_by_identifier(identifier: Identifier) -> Optional[str]:
    params = {
        'identifier': f'{identifier.system}|{identifier.value}'
    }

    try:
        response = requests.get(FHIR_ORGANIZATION_URL, params=params, timeout=TIMEOUT_DEFAULT)
        
        if response.status_code == 200:
            data = response.json()
            
            if "entry" in data:
                return data["entry"][0]["resource"]
        return None
    
    except requests.exceptions.Timeout:
        print(f"Timeout ao acessar {FHIR_ORGANIZATION_URL}")
    except requests.exceptions.RequestException:
        print(f"Erro ao acessar {FHIR_ORGANIZATION_URL}")
    except Exception as e:
        print(f"Erro inesperado ao acessar {FHIR_ORGANIZATION_URL}: {e}")
    
    return None

async def get_organization_by_system_value(system: str, value: str) -> Optional[str]:
    if  system and value:
        identifier = Identifier(system=system, value=value)
        return await get_organization_by_identifier(identifier)
    
    return None

async def get_organization_by_cnpj(cnpj: str):
    return await get_organization_by_system_value(CNPJ_SYSTEM, cnpj)

async def get_organization_id_by_cnpj(cnpj: str):
    organization = await get_organization_by_cnpj(cnpj)
    if organization:
        return organization['id']
    return None