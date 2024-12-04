from dataclasses import dataclass
from typing import Optional
import datetime
from fhir.resources.R4B.contactpoint import ContactPoint
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.location import Location
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.fhirprimitiveextension import FHIRPrimitiveExtension
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.reference import Reference
from kafka_fhir_adapter.services.fhir_organization import get_organization_id_by_identifier_cnpj


@dataclass
class LocationResource:
    id: None 
    data_atualizacao_tasy: None 
    codigo_setor_atendimento: Optional[str]
    codigo_centro_custo: Optional[str]
    status: Optional[str]
    nome_setor_atendimento: Optional[str]
    telefone: Optional[str]
    cnpj_estabelecimento: Optional[str]
    pais: Optional[str]
    estado: Optional[str]
    cidade: Optional[str]
    cep: Optional[str]
    bairro: Optional[str]
    complemento: Optional[str]
    numero: Optional[str]
    logradouro: Optional[str]
    tipo_logradouro: Optional[str]

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id=None,
            data_atualizacao_tasy=None,
            codigo_setor_atendimento=message.get('CODIGO_SETOR_ATENDIMENTO',None),
            codigo_centro_custo=message.get('CODIGO_CENTRO_CUSTO',None),
            status=message.get('STATUS',None),
            nome_setor_atendimento=message.get("NOME_SETOR_ATENDIMENTO",None),
            telefone=message.get("TELEFONE",None),
            cnpj_estabelecimento=message.get("CNPJ_ESTABELECIMENTO",None),
            tipo_logradouro=message.get('TIPO_LOGRADOURO', None),
            logradouro=message.get('LOGRADOURO', None),
            numero=message.get('NUMERO', None),
            complemento=message.get('COMPLEMENTO', None),
            bairro=message.get('BAIRRO', None),
            cidade=message.get('CIDADE', None),
            estado=message.get('ESTADO', None),
            pais=message.get('PAIS', None),
            cep=message.get('CEP', None),
    )

    async def to_fhir(self):
        location = Location(
            name=self.nome_setor_atendimento,
            identifier=[],
            telecom=[],
            extension=[]
        )

        meta = Meta(
            profile=[
                "https://fhir.omnisaude.co/r4/core/StructureDefinition/location"
            ]
        )
        location.meta = meta

        if self.status:
            location.status = self.status.lower()

        if self.telefone:
            telecom = ContactPoint(
                system="phone",
                value=self.telefone,
            )
            location.telecom.append(telecom)

        if self.cnpj_estabelecimento:
            id_organization = await get_organization_id_by_identifier_cnpj(self.cnpj_estabelecimento)
            reference = Reference(
                reference=f"Organization/{id_organization}"
            )
        location.managingOrganization = reference

        address = Address(
            country=self.pais,
            state=self.estado,
            city=self.cidade,
            postalCode=self.cep,
            line=[
                self.bairro,
                self.complemento,
                self.numero,
                self.logradouro,
                self.tipo_logradouro
            ],
            _line=[
                FHIRPrimitiveExtension(id="bairro", extension=[]),
                FHIRPrimitiveExtension(id="complemento", extension=[]),
                FHIRPrimitiveExtension(id="numero", extension=[]),
                FHIRPrimitiveExtension(id="logradouro", extension=[]),
                FHIRPrimitiveExtension(id="tipoLogradouro", extension=[])
            ]
        )
        location.address = address

        return location