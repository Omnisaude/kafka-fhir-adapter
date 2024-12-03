from dataclasses import dataclass
from typing import Optional

from fhir.resources.R4B.contactpoint import ContactPoint
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.organization import Organization
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.fhirprimitiveextension import FHIRPrimitiveExtension
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.period import Period

from kafka_fhir_adapter.services.fhir import string_to_bool


@dataclass
class OrganizationResource:
    id: Optional[str]
    nome_principal: Optional[str]
    ativo: Optional[bool]
    cnpj: Optional[str]
    nome_alternativo_1: Optional[str]
    nome_alternativo_2: Optional[str]
    telefone: Optional[str]
    pais: Optional[str]
    estado: Optional[str]
    cidade: Optional[str]
    cep: Optional[str]
    bairro: Optional[str]
    complemento: Optional[str]
    numero: Optional[str]
    logradouro: Optional[str]
    tipo_logradouro: Optional[str]
    cnae: Optional[str]
    data_inicio: Optional[str]
    data_atualizacao_tasy: [str]

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id=None,
            nome_principal=message.get('NOME_PRINCIPAL', None),
            ativo = string_to_bool(message.get('ATIVO', 'False')),
            cnpj = message.get('CNPJ', None),
            nome_alternativo_1 = message.get('NOME_ALTERNATIVO_1', None),
            nome_alternativo_2 = message.get('NOME_ALTERNATIVO_2', None),
            telefone = message.get('TELEFONE', None),
            pais = message.get('PAIS', None),
            estado = message.get('ESTADO', None),
            cidade = message.get('CIDADE', None),
            cep = message.get('CEP', None),
            bairro = message.get('BAIRRO', None),
            complemento = message.get('COMPLEMENTO', None),
            numero = message.get('NUMERO', None),
            logradouro = message.get('LOGRADOURO', None),
            tipo_logradouro = message.get('TIPO_LOGRADOURO', None),
            cnae = message.get('CNAE', None),
            data_inicio = message.get('DATA_INICIO', None),
            data_atualizacao_tasy=None
        )

    def to_fhir(self):
        organization = Organization(
            # id="UTIIOP", // o servico ignora o id passado
            name=self.nome_principal,
            alias=[],
            identifier=[],
            address=[],
            telecom=[],
            extension=[]
        )

        meta = Meta(
            profile=[
                "https://fhir.omnisaude.co/r4/core/StructureDefinition/organizacao"
            ]
        )
        organization.meta = meta

        if self.ativo:
            organization.active = self.ativo

        identifier = Identifier(
            system="https://fhir.omnisaude.co/r4/core/sid/cnpj",
            value=self.cnpj,
        )
        organization.identifier.append(identifier)

        alias = []
        if self.nome_alternativo_1:
            alias.append(self.nome_alternativo_1)
        if self.nome_alternativo_2:
            alias.append(self.nome_alternativo_2)
        organization.alias = alias

        telecom = ContactPoint(
            system="phone",
            value=self.telefone,
        )
        organization.telecom.append(telecom)

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
        organization.address.append(address)

        if self.cnae:
            extension_cnae = Extension(
                url="https://fhir.omnisaude.co/r4/core/StructureDefinition/cnae",
                extension=[
                    Extension(url="principal", valueCode=self.cnae)
                ]
            )
            organization.extension.append(extension_cnae)

        if self.data_inicio:
            # do kakfa as datas vem em milisegundos em utc timestamp.
            # para converter essas datas precisa passar para segundos e entao usar a funcao
            extension_organization_period = Extension(
                url="http://hl7.org/fhir/StructureDefinition/organization-period",
                valuePeriod=Period(start=self.data_inicio)
            )
            organization.extension.append(extension_organization_period)

        return organization