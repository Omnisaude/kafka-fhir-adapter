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


from typing import Optional
from dataclasses import dataclass

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
    cep: Optional[str]
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
            cep=message.get('CEP', None),
            endereco_completo=message.get('ENDERECO_COMPLETO', None),
    )

    def to_fhir(self) -> Patient:
        patient = Patient(
            meta= Meta(profile=["https://fhir.omnisaude.co/r4/core/StructureDefinition/paciente"])
        )

        if self.nome_paciente:
            patient.name = [HumanName(text=self.nome_paciente)]

        if self.data_nascimento:
            patient.birthDate = self.data_nascimento

        # Gênero
        if self.codigo_sexo:
            patient.gender = self.codigo_sexo.lower()

        # Identificadores
        identifiers = []
        if self.prontuario:
            identifiers.append(Identifier(
                system="https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health",
                value=self.prontuario
            ))

        if self.cpf:
            identifiers.append(Identifier(
                system="https://fhir.omnisaude.co/r4/core/sid/cpf",
                value=self.cpf
            ))

        if self.cartao_nacional_saude:
            identifiers.append(Identifier(
                system="https://fhir.omnisaude.co/r4/core/sid/cns",
                value=self.cartao_nacional_saude
            ))

        if identifiers:
            patient.identifier = identifiers

        # Extensões
        extensions = []
        if self.nome_mae:
            extensions.append(Extension(
                url="http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName",
                valueString=self.nome_mae
            ))

        if self.nome_pai:
            extensions.append(Extension(
                url="https://fhir.omnisaude.co/r4/core/StructureDefinition/nome-pai-paciente",
                valueString=self.nome_pai
            ))

        if self.codigo_nacionalidade:
            coding_nacionalidade = Coding(
                system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRPais",
                code=self.codigo_nacionalidade
            )
            codeable_concept_nacionalidade = CodeableConcept(coding=[coding_nacionalidade])
            extensions.append(Extension(
                url="http://hl7.org/fhir/StructureDefinition/patient-nationality",
                extension=[
                    Extension(url="code", valueCodeableConcept=codeable_concept_nacionalidade)
                ]
            ))

        if self.codigo_raca or self.codigo_etnia:
            extension_raca_cor_etnia = Extension(
                url="http://www.saude.gov.br/fhir/r4/StructureDefinition/BRRacaCorEtnia-1.0",
                extension=[]
            )
            
            if self.codigo_raca:
                coding_raca = Coding(
                    system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRRacaCor",
                    code=self.codigo_raca
                )
                
                codeable_concept_raca = CodeableConcept(coding=[coding_raca])
                
                extension_raca_cor_etnia.extension.append(Extension(url="race", valueCodeableConcept=codeable_concept_raca))


            if self.codigo_etnia:
                coding_etnia = Coding(
                    system="http://www.saude.gov.br/fhir/r4/CodeSystem/BREtniaIndigena",
                    code=self.codigo_etnia
                )
                
                codeable_concept_etnia = CodeableConcept(coding=[coding_etnia])
                
                extension_raca_cor_etnia.extension.append(Extension(url="indigenousEthnicity", valueCodeableConcept=codeable_concept_etnia))
                
                
            extensions.append(extension_raca_cor_etnia)
                
        if extensions:
            patient.extension = extensions

        if self.telefone:
            patient.telecom = [ContactPoint(system="phone", value=self.telefone)]
            
        endereco = self.create_address()
        
        if not is_address_empty(endereco):
            patient.address=[]
            patient.address.append(endereco)

        return patient
    

    def create_address(self) -> Address:
        address = Address()
        
        if self.codigo_pais:
            address.country = self.codigo_pais
        
        if self.codigo_ibge_estado:
            address.state = self.codigo_ibge_estado
        
        if self.codigo_ibge_cidade:
            address.city = self.codigo_ibge_cidade
        
        if self.cep:
            address.postalCode = self.cep
        
        if self.endereco_completo:
            address.text = self.endereco_completo
        
        line=[]
        _line=[]
        
        if self.codigo_tipo_logradouro:
            line.append(self.codigo_tipo_logradouro)
            _line.append(FHIRPrimitiveExtension(id="tipoLogradouro", extension=[]))
        
        if self.logradouro:
            line.append(self.logradouro)
            _line.append(FHIRPrimitiveExtension(id="logradouro", extension=[]))
        
        if self.numero:
            line.append(self.numero)
            _line.append(FHIRPrimitiveExtension(id="numero", extension=[]))
            
        if self.complemento:
            line.append(self.complemento)
            _line.append(FHIRPrimitiveExtension(id="complemento", extension=[]))
            
        if self.bairro:
            line.append(self.bairro)
            _line.append(FHIRPrimitiveExtension(id="bairro", extension=[]))
        
        if line:    
            address.line=line
            address.line__ext=_line
        
        return address
        
def is_address_empty(address: Address) -> bool:
    if any([
            address.use,
            address.type,
            address.text,
            address.line,
            address.city,
            address.district,
            address.state,
            address.postalCode,
            address.country,
            address.period
            ]):
        return False

    return True


export = is_address_empty, PatientResource