import requests
from config import FHIR_SERVER_URL

async def get_organization_id_by_identifier_cnpj(identifier: str = None):
    # Monta a query para buscar pelo identifier
    query = f"{FHIR_SERVER_URL}/fhir/Organization?identifier=https://fhir.omnisaude.co/r4/core/sid/cnpj|{identifier}"

    # Faz a requisição ao servidor FHIR
    response = requests.get(query)

    if response.status_code == 200:
        data = response.json()
        if "entry" in data and len(data["entry"]) > 0:
            # Retorna o ID do primeiro recurso encontrado
            return data["entry"][0]["resource"]["id"]