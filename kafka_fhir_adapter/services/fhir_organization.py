import requests
from config import FHIR_SERVER_URL
from faust.app import App

async def get_organization_id_by_identifier_cnpj(identifier: str):
    # Monta a query para buscar pelo identifier
    url = f"{FHIR_SERVER_URL}/fhir/Organization?identifier=https://fhir.omnisaude.co/r4/core/sid/cnpj|{identifier}"
    # Faz a requisição ao servidor FHIR

    response = await requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "entry" in data and len(data["entry"]) > 0:
            # Retorna o ID do primeiro recurso encontrado
            return data["entry"][0]["resource"]["id"]
    return None