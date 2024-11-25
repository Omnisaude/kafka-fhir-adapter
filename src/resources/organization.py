import datetime

from fhir.resources.R4B.contactpoint import ContactPoint
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.organization import Organization
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.fhirprimitiveextension import FHIRPrimitiveExtension
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.period import Period

from src.fhir_service import epoch_timestamp_to_iso_string


def init_organization(message: dict) -> str:
    organization = Organization(
        # id="UTIIOP", // o servico ignora o id passado
        name=message.get('NOME_PRINCIPAL', {}).get('string', None),
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

    if message.get('ATIVO', False):
        organization.active = bool(message.get('ATIVO', False))

    identifier = Identifier(
        system="https://fhir.omnisaude.co/r4/core/sid/cnpj",
        value=message.get('CNPJ', None),
    )
    organization.identifier.append(identifier)

    alias = []
    if message.get('NOME_ALTERNATIVO_1', None):
        alias.append(message.get('NOME_ALTERNATIVO_1'))
    if message.get('NOME_ALTERNATIVO_2', None):
        alias.append(message.get('NOME_ALTERNATIVO_2'))
    organization.alias = alias

    telecom = ContactPoint(
        system="phone",
        value=message.get('TELEFONE', {}).get('string', None),
    )
    organization.telecom.append(telecom)

    address = Address(
        country=message.get('PAIS', {}).get('string', None),
        state=message.get('ESTADO', {}).get('string', None),
        city=message.get('CIDADE', {}).get('string', None),
        postalCode=message.get('CEP', {}).get('string', None),
        line=[
            message.get('BAIRRO', {}).get('string', None),
            message.get('COMPLEMENTO', {}).get('string', None),
            message.get('NUMERO', {}).get('string', None),
            message.get('LOGRADOURO', {}).get('string', None),
            message.get('TIPO_LOGRADOURO', {}).get('string', None),
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

    if message.get('CNAE', None):
        extension_cnae = Extension(
            url="https://fhir.omnisaude.co/r4/core/StructureDefinition/cnae",
            extension=[
                Extension(url="principal", valueCode=message.get('CNAE').get('string', None))
            ]
        )
        organization.extension.append(extension_cnae)

    if message.get('DATA_INICIO', None):
        # do kakfa as datas vem em milisegundos em utc timestamp.
        # para converter essas datas precisa passar para segundos e entao usar a funcao
        extension_organization_period= Extension(
            url="http://hl7.org/fhir/StructureDefinition/organization-period",
            valuePeriod=Period(start=epoch_timestamp_to_iso_string(message.get('DATA_INICIO', {}).get('long', None)))
        )
        organization.extension.append(extension_organization_period)

    return organization.json()