import requests

from fhir.resources.R4B.identifier import Identifier

from typing import Optional

from kafka_fhir_adapter.config import FHIR_BASE_URL


FHIR_PATIENT_URL = f"{FHIR_BASE_URL}/Patient"
TIMEOUT_DEFAULT = 10

CPF_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/cpf"
CNS_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/cns"
PRONTUARIO_AMH_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health"

def get_patient_by_identifier(identifier: Identifier) -> Optional[str]:
    url = f"{FHIR_PATIENT_URL}?identifier={identifier.system}|{identifier.value}"
    
    params = {
        'identifier': f'{identifier.system}|{identifier.value}'
    }

    try:
        response = requests.get(url, params=params, timeout=TIMEOUT_DEFAULT)

        if response.status_code == 200:
            data = response.json()
            
            if "entry" in data and len(data["entry"]) == 1:
                return data["entry"][0]["resource"]
        return None
    
    except requests.exceptions.Timeout:
        print(f"Timeout ao acessar {url}")
    except requests.exceptions.RequestException:
        print(f"Erro ao acessar {url}")
    except Exception as e:
        print(f"Erro inesperado ao acessar {url}: {e}")
    
    return None

def get_patient_by_system_value(system: str, value: str) -> Optional[str]:
    if  system and value:
        identifier = Identifier(system=system, value=value)
        return get_patient_by_identifier(identifier)
    
    return None

def get_patient_by_cpf(cpf: str) -> Optional[str]:
    return get_patient_by_system_value(CPF_SYSTEM, cpf)

def get_patient_by_cns(cns: str) -> Optional[str]:
    return get_patient_by_system_value(CNS_SYSTEM, cns)

def get_patient_by_prontuario_amh(prontuario_amh: str) -> Optional[str]:
    return get_patient_by_system_value(PRONTUARIO_AMH_SYSTEM, prontuario_amh)
