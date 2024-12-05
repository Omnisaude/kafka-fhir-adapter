import requests

from kafka_fhir_adapter.config import FHIR_BASE_URL


FHIR_LOCATION_URL = f"{FHIR_BASE_URL}/Location"
TIMEOUT_DEFAULT = 10


async def get_location_by_name_and_organization_id():
    return None

async def get_location_by_location_name_and_organization_id(name: str, organization_id: str):
    params = {
        'name': name,
        'organization': f'Organization/{organization_id}'
    }
    
    try:
        response = requests.get(FHIR_LOCATION_URL, params=params, timeout=TIMEOUT_DEFAULT)
        
        if response.status_code == 200:
            data = response.json()
            
            if "entry" in data:
                return data["entry"][0]["resource"]
        return None

    except requests.exceptions.Timeout:
        print(f"Timeout ao acessar {FHIR_LOCATION_URL}")
    except requests.exceptions.RequestException:
        print(f"Erro ao acessar {FHIR_LOCATION_URL}")
    except Exception as e:
        print(f"Erro inesperado ao acessar {FHIR_LOCATION_URL}: {e}")
    
    return None

async def get_location_id_by_name_and_organization_id(name: str, organization_id: str):
    location = await get_location_by_location_name_and_organization_id(name, organization_id)
    if location:
        return location['id']
    return None