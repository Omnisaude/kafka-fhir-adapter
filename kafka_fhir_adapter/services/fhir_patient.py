import requests

from fhir.resources.R4B.identifier import Identifier

from typing import Optional

from kafka_fhir_adapter.config import FHIR_BASE_URL


FHIR_PATIENT_URL = f"{FHIR_BASE_URL}/Patient"
TIMEOUT_DEFAULT = 10

CPF_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/cpf"
CNS_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/cns"
PRONTUARIO_AMH_SYSTEM = "https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health"

async def get_patient_by_identifier(identifier: Identifier) -> Optional[str]:
    params = {
        'identifier': f'{identifier.system}|{identifier.value}'
    }

    try:
        response = requests.get(FHIR_PATIENT_URL, params=params, timeout=TIMEOUT_DEFAULT)

        if response.status_code == 200:
            data = response.json()
            
            if "entry" in data:
                return data["entry"][0]["resource"]
        return None
    
    except requests.exceptions.Timeout:
        print(f"Timeout ao acessar {FHIR_PATIENT_URL}")
    except requests.exceptions.RequestException:
        print(f"Erro ao acessar {FHIR_PATIENT_URL}")
    except Exception as e:
        print(f"Erro inesperado ao acessar {FHIR_PATIENT_URL}: {e}")
    
    return None

async def get_patient_by_system_value(system: str, value: str) -> Optional[str]:
    if  system and value:
        identifier = Identifier(system=system, value=value)
        return await get_patient_by_identifier(identifier)
    
    return None

async def get_patient_by_cpf(cpf: str) -> Optional[str]:
    return await get_patient_by_system_value(CPF_SYSTEM, cpf)

async def get_patient_by_cns(cns: str) -> Optional[str]:
    return await get_patient_by_system_value(CNS_SYSTEM, cns)

async def get_patient_by_prontuario_amh(prontuario_amh: str) -> Optional[str]:
    return await get_patient_by_system_value(PRONTUARIO_AMH_SYSTEM, prontuario_amh)

async def get_patient_id_by_cpf(cpf: str) -> Optional[str]:
    patient = await get_patient_by_cpf(cpf)
    if patient:
        return patient["id"]
    return None

async def get_patient_id_by_prontuario_amh(prontuario_amh: str) -> Optional[str]:
    patient = await get_patient_by_prontuario_amh(prontuario_amh)
    if patient:
        return patient["id"]
    return None

async def get_patient_id_by_cns(cns: str) -> Optional[str]:
    patient = await get_patient_by_cns(cns)
    if patient:
        return patient["id"]
    return None

async def get_patient_id(cpf: str = None, cns: str = None, prontuario_amh: str = None) -> Optional[str]:
    patient_id = None
    if cpf:
        patient_id = await get_patient_id_by_cpf(cpf)

    if not patient_id and cns:
        patient_id = await get_patient_id_by_cns(cns)

    if not patient_id and prontuario_amh:
        patient_id = await get_patient_id_by_prontuario_amh(prontuario_amh)

    return patient_id
