import json
import pytest
from kafka_fhir_adapter.resources.practitioner_role import PractitionerRoleResource

complete_message_practitioner_role = '''{
    "PRACTITIONER_ROLE_KEY": "123456",
    "PRACTITIONER_ROLE_CPF": "03276299359",
    "PRACTITIONER_ROLE_DATA_ATUALIZACAO": "2024-01-01",
    "PRACTITIONER_ROLE_CD_CBO": "225125",
    "PRACTITIONER_ROLE_NOME_CBO": "Médico Clínico",
    "PRACTITIONER_CODIGO_ESPECIALIDADE_MEDICA": "1234",
    "PRACTITIONER_ESPECIALIDADE_MEDICA": "Clínica Médica"
}'''


async def test_create_practitioner_role_complete():
    message = json.loads(complete_message_practitioner_role)
    practitioner_role_resource = PractitionerRoleResource.from_dict(message)
    practitioner_role = await practitioner_role_resource.to_fhir()

    assert practitioner_role is not None
    assert practitioner_role.meta.profile[0] == "https://fhir.omnisaude.co/r4/core/StructureDefinition/papel-profissional"
    assert practitioner_role.code[0].coding[0].code == "225125"
    assert practitioner_role.code[0].coding[0].display == "Médico Clínico"
    assert practitioner_role.active is True
