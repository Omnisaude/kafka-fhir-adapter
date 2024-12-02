import datetime
from fhir.resources.R4B.contactpoint import ContactPoint
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.humanname import HumanName
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.fhirprimitiveextension import FHIRPrimitiveExtension
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.period import Period


# from fhir_service import epoch_timestamp_to_iso_string, string_to_bool


def init_patient(message: dict) -> str:
    patient = Patient(
        name=[
            HumanName(
                text=message.get('NOME_PACIENTE', None),
            )
        ],
        identifier=[],
        extension=[],
        telecom=[],
        address=[]
    )

    meta = Meta(
        profile=[
            "https://fhir.omnisaude.co/r4/core/StructureDefinition/paciente"
        ]
    )
    patient.meta = meta

    if message.get('DATA_NASCIMENTO', None):
        patient_birthDate = message.get('DATA_NASCIMENTO', None)
        patient.birthDate = patient_birthDate

    if message.get('CODIGO_SEXO', None):
        patient_sexo = message.get('CODIGO_SEXO', None)
        patient.gender = patient_sexo.lower()

    if message.get('PRONTUARIO', None):
        identifier_prontuario = Identifier(
            system="https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health",
            value=message.get('PRONTUARIO', None)
        )
        patient.identifier.append(identifier_prontuario)

    if message.get('CPF', None):
        identifier_cpf = Identifier(
            system="https://fhir.omnisaude.co/r4/core/sid/cpf",
            value=message.get('CPF', None)
        )
        patient.identifier.append(identifier_cpf)

    if message.get('CARTAO_NACIONAL_SAUDE', None):
        identifier_cns = Identifier(
            system="https://fhir.omnisaude.co/r4/core/sid/cns",
            value=message.get('CARTAO_NACIONAL_SAUDE', None)
        )
        patient.identifier.append(identifier_cns)

    if message.get("NOME_MAE", None):
        extension_mae = Extension(
            url="http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName",
            valueString=message.get('NOME_MAE', None)
        )
        patient.extension.append(extension_mae)

    if message.get("NOME_PAI", None):
        extension_pai = Extension(
            url="https://fhir.omnisaude.co/r4/core/StructureDefinition/nome-pai-paciente",
            valueString=message.get('NOME_PAI', None)
        )
        patient.extension.append(extension_pai)

    if message.get("CODIGO_NACIONALIDADE", None):
        coding_nacionalidade = Coding(
            system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRPais",
            # Sistema de codificação (SNOMED CT por exemplo)
            code=message.get("CODIGO_NACIONALIDADE", None),  # Código que representa um conceito
        )

        codeable_concept_nacionalidade = CodeableConcept(
            coding=[coding_nacionalidade],  # Lista de codificações, pois pode ter múltiplas
        )

        extension_nacionalidade = Extension(
            url="http://hl7.org/fhir/StructureDefinition/patient-nationality",
            extension=[
                Extension(url="code", valueCodeableConcept=codeable_concept_nacionalidade)
                # Corrigir para usar valueCode
            ]
        )

        patient.extension.append(extension_nacionalidade)

    if message.get("CODIGO_RACA", None):
        coding_raca = Coding(
            system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRRacaCor",
            # Sistema de codificação (SNOMED CT por exemplo)
            code=message.get("CODIGO_RACA", None),  # Código que representa um conceito
        )

        codeable_concept_raca = CodeableConcept(
            coding=[coding_raca],  # Lista de codificações, pois pode ter múltiplas
        )

        extension_raca = Extension(
            url="http://www.saude.gov.br/fhir/r4/StructureDefinition/BRRacaCorEtnia-1.0",
            extension=[
                Extension(url="race", valueCodeableConcept=codeable_concept_raca)
            ]
        )
        patient.extension.append(extension_raca)

    if message.get("CODIGO_ETNIA", None):
        coding_etnia = Coding(
            system="http://www.saude.gov.br/fhir/r4/CodeSystem/BREtniaIndigena",
            # Sistema de codificação (SNOMED CT por exemplo)
            code=message.get("CODIGO_ETNIA", None),  # Código que representa um conceito
        )

        codeable_concept_etnia = CodeableConcept(
            coding=[coding_etnia],  # Lista de codificações, pois pode ter múltiplas
        )

        extension_etnia = Extension(
            url="http://www.saude.gov.br/fhir/r4/StructureDefinition/BRRacaCorEtnia-1.0",
            extension=[
                Extension(url="indigenousEthnicity", valueCodeableConcept=codeable_concept_etnia)
            ]
        )
        patient.extension.append(extension_etnia)

    if message.get("TELEFONE"):
        telecom = ContactPoint(
            system="phone",
            value=message.get('TELEFONE', None),
        )
        patient.telecom.append(telecom)

    line_values = [
        ("BAIRRO", "bairro"),
        ("COMPLEMENTO", "complemento"),
        ("NUMERO", "numero"),
        ("LOGRADOURO", "logradouro"),
        ("TIPO_LOGRADOURO", "tipoLogradouro"),
    ]

    line = []
    _line = []

    # Iterar pelos valores e adicionar apenas os existentes
    for field, field_id in line_values:
        value = message.get(field)  # Obter o valor do campo no dicionário
        if value:  # Adicionar à lista somente se o valor for válido (não vazio)
            line.append(value)
            _line.append(FHIRPrimitiveExtension(id=field_id, extension=[]))

    # Criar o Address com verificação para `line` e `_line`
    address = Address(
        country=message.get("CODIGO_PAIS"),
        state=message.get("CODIGO_IBGE_ESTADO"),
        city=message.get("CODIGO_IBGE_CIDADE"),
        postalCode=message.get("CEP"),
        text=message.get("ENDERECO_COMPLETO"),
        line=line if line else None,  # Somente incluir `line` se tiver valores
        _line=_line if _line else None,  # Somente incluir `_line` se tiver valores
    )

    # Garantir que a lista de endereços do paciente exista
    if not hasattr(patient, "address") or patient.address is None:
        patient.address = []

    # Adicionar o endereço à lista do paciente
    patient.address.append(address)

    return patient.json()