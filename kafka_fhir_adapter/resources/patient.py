import datetime
from dataclasses import dataclass
from typing import Optional
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
@dataclass
class PatientResource:
    id: Optional[str]
    codigo_pessoa_fisica: Optional[str]
    data_atualizacao_tasy: Optional[str]
    nome_pai: Optional[str]
    nome_mae: Optional[str]
    codigo_nacionalidade: Optional[str]
    codigo_raca: Optional[str]
    codigo_etnia: Optional[str]
    prontuario: Optional[str]
    cpf: Optional[str]
    cartao_nacional_saude: Optional[str]
    nome_paciente: Optional[str]
    codigo_sexo: Optional[str]
    data_nascimento: Optional[str]
    telefone: Optional[str]
    estado_civil: Optional[str]
    codigo_tipo_logradouro: Optional[str]
    logradouro: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    codigo_ibge_cidade: Optional[str]
    codigo_ibge_estado: Optional[str]
    codigo_pais: Optional[str]
    codigo_cep: Optional[str]
    endereco_completo: Optional[str]

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id=None,
            codigo_pessoa_fisica=message.get('CODIGO_PESSOA_FISICA', None),
            data_atualizacao_tasy=None,
            nome_pai=message.get('NOME_PAI', None),
            nome_mae=message.get('NOME_MAE', None),
            codigo_nacionalidade=message.get('CODIGO_NACIONALIDADE', None),
            codigo_raca=message.get('CODIGO_RACA', None),
            codigo_etnia=message.get('CODIGO_ETNIA', None),
            prontuario=message.get('PRONTUARIO', None),
            cpf=message.get('CPF', None),
            cartao_nacional_saude=message.get('CARTAO_NACIONAL_SAUDE', None),
            nome_paciente=message.get('NOME_PACIENTE', None),
            codigo_sexo=message.get('CODIGO_SEXO', None),
            data_nascimento=message.get('DATA_NASCIMENTO', None),
            telefone=message.get('TELEFONE', None),
            estado_civil=message.get('ESTADO_CIVIL', None),
            codigo_tipo_logradouro=message.get('CODIGO_TIPO_LOGRADOURO', None),
            logradouro=message.get('LOGRADOURO', None),
            numero=message.get('NUMERO', None),
            complemento=message.get('COMPLEMENTO', None),
            bairro=message.get('BAIRRO', None),
            codigo_ibge_cidade=message.get('CODIGO_IBGE_CIDADE', None),
            codigo_ibge_estado=message.get('CODIGO_IBGE_ESTADO', None),
            codigo_pais=message.get('CODIGO_PAIS', None),
            codigo_cep=message.get('CODIGO_CEP', None),
            endereco_completo=message.get('ENDERECO_COMPLETO', None),
    )

    def to_fhir(self):
        patient = Patient(
            name=[
                HumanName(
                    text=self.nome_paciente,
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

        if self.data_nascimento:
            patient_birthDate = self.data_nascimento
            patient.birthDate = patient_birthDate

        if self.codigo_sexo:
            patient_sexo = self.codigo_sexo
            patient.gender = patient_sexo.lower()

        if self.prontuario:
            identifier_prontuario = Identifier(
                system="https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health",
                value=self.prontuario
            )
            patient.identifier.append(identifier_prontuario)

        if self.cpf:
            identifier_cpf = Identifier(
                system="https://fhir.omnisaude.co/r4/core/sid/cpf",
                value=self.cpf
            )
            patient.identifier.append(identifier_cpf)

        if self.cartao_nacional_saude:
            identifier_cns = Identifier(
                system="https://fhir.omnisaude.co/r4/core/sid/cns",
                value=self.cartao_nacional_saude
            )
            patient.identifier.append(identifier_cns)

        if self.nome_mae:
            extension_mae = Extension(
                url="http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName",
                valueString=self.nome_mae
            )
            patient.extension.append(extension_mae)

        if self.nome_pai:
            extension_pai = Extension(
                url="https://fhir.omnisaude.co/r4/core/StructureDefinition/nome-pai-paciente",
                valueString=self.nome_pai
            )
            patient.extension.append(extension_pai)

        if self.codigo_nacionalidade:
            coding_nacionalidade = Coding(
                system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRPais",
                # Sistema de codificação (SNOMED CT por exemplo)
                code=self.codigo_nacionalidade,  # Código que representa um conceito
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

        if self.codigo_raca:
            coding_raca = Coding(
                system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRRacaCor",
                # Sistema de codificação (SNOMED CT por exemplo)
                code=self.codigo_raca,  # Código que representa um conceito
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

        if self.codigo_etnia:
            coding_etnia = Coding(
                system="http://www.saude.gov.br/fhir/r4/CodeSystem/BREtniaIndigena",
                # Sistema de codificação (SNOMED CT por exemplo)
                code=self.codigo_etnia,  # Código que representa um conceito
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

        if self.telefone:
            telecom = ContactPoint(
                system="phone",
                value=self.telefone,
            )
            patient.telecom.append(telecom)

        address = Address(
            country=self.codigo_pais,
            state=self.codigo_ibge_estado,
            city=self.codigo_ibge_cidade,
            postalCode=self.codigo_cep,
            line=[
                self.bairro,
                self.complemento,
                self.numero,
                self.logradouro,
                self.codigo_tipo_logradouro
            ],
            _line=[
                FHIRPrimitiveExtension(id="bairro", extension=[]),
                FHIRPrimitiveExtension(id="complemento", extension=[]),
                FHIRPrimitiveExtension(id="numero", extension=[]),
                FHIRPrimitiveExtension(id="logradouro", extension=[]),
                FHIRPrimitiveExtension(id="tipoLogradouro", extension=[])
            ]
        )
        patient.address.append(address)

        return patient