from dataclasses import dataclass
from typing import Optional

from fhir.resources.R4B.practitionerrole import PractitionerRole
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.reference import Reference

from kafka_fhir_adapter.services.fhir_practitioner import *

@dataclass
class PractitionerRoleResource:
    id: Optional[str]
    practitioner_role_key: Optional[str]
    practitioner_role_cpf: Optional[str]
    practitioner_role_data_atualizacao: Optional[str]
    practitioner_role_cd_cbo: Optional[str]
    practitioner_role_nome_cbo: Optional[str]
    practitioner_codigo_especialidade_medica: Optional[str]
    practitioner_especialidade_medica: Optional[str]

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id=None,
            practitioner_role_key=message.get('PRACTITIONER_ROLE_KEY', None),
            practitioner_role_cpf=message.get('PRACTITIONER_ROLE_CPF', None),
            practitioner_role_data_atualizacao=message.get('PRACTITIONER_ROLE_DATA_ATUALIZACAO', None),
            practitioner_role_cd_cbo=message.get('PRACTITIONER_ROLE_CD_CBO', None),
            practitioner_role_nome_cbo=message.get('PRACTITIONER_ROLE_NOME_CBO', None),
            practitioner_codigo_especialidade_medica=message.get('PRACTITIONER_CODIGO_ESPECIALIDADE_MEDICA', None),
            practitioner_especialidade_medica=message.get('PRACTITIONER_ESPECIALIDADE_MEDICA', None)
        )

    async def to_fhir(self) -> Optional[PractitionerRole]:
        practitioner_role = PractitionerRole(
            identifier=[],
            code=[],
            specialty=[],
            extension=[]
        )

        # Set meta
        meta = Meta(
            profile=[
                "https://fhir.omnisaude.co/r4/core/StructureDefinition/papel-profissional"
            ]
        )
        practitioner_role.meta = meta

        if not self.practitioner_role_cpf:
            return None

        practitioner_id = await get_practitioner_id_by_cpf(self.practitioner_role_cpf)

        if not practitioner_id:
            return None

        practitioner_role.practitioner = Reference(
            reference=f"Practitioner/{practitioner_id}"
        )
        
        if self.practitioner_role_cd_cbo and self.practitioner_role_nome_cbo:
            cbo_coding = Coding(
                system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRCBO",
                code=self.practitioner_role_cd_cbo,
                display=self.practitioner_role_nome_cbo
            )
            practitioner_role.code = [CodeableConcept(coding=[cbo_coding])]

        practitioner_role.active = True

        return practitioner_role