from dataclasses import dataclass
from typing import Optional

from fhir.resources.R4B.practitioner import Practitioner
from fhir.resources.R4B.humanname import HumanName
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.contactpoint import ContactPoint
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.fhirprimitiveextension import FHIRPrimitiveExtension
from fhir.resources.R4B.period import Period
from fhir.resources.R4B.extension import Extension

@dataclass
class PractitionerResource:
    id: Optional[str]
    codigo_pessoa_fisica: Optional[str]
    nome_profissional: Optional[str]
    cpf: Optional[str]
    data_nascimento: Optional[str]
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
    nr_conselho: Optional[str]
    codigo_sexo: Optional[str]
    telefone: Optional[str]
    data_atualizacao: Optional[str]

    @classmethod
    def from_dict(cls, message: dict):
        return cls(
            id=None,
            codigo_pessoa_fisica=message.get('CD_PESSOA_FISICA', None),
            nome_profissional=message.get('NOME_PROFISSIONAL', None),
            cpf=message.get('CPF', None),
            data_nascimento=message.get('DATA_NASCIMENTO', None),
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
            nr_conselho=message.get('NR_CONSELHO', None),
            codigo_sexo=message.get('CODIGO_SEXO', None),
            telefone=message.get('TELEFONE', None),
            data_atualizacao=message.get('DATA_ATUALIZACAO', None)
        )

    def to_fhir(self) -> Practitioner:
        practitioner = Practitioner(
            name=[],
            identifier=[],
            address=[],
            telecom=[],
            extension=[]
        )

        meta = Meta(
            profile=[
                "https://fhir.omnisaude.co/r4/core/StructureDefinition/profissional"
            ]
        )
        practitioner.meta = meta

        if self.nome_profissional:
            name = HumanName(
                text=self.nome_profissional
            )
            practitioner.name.append(name)

        if self.cpf:
            identifier_cpf = Identifier(
                system="https://fhir.omnisaude.co/r4/core/sid/cpf",
                value=self.cpf
            )
            practitioner.identifier.append(identifier_cpf)

        if self.codigo_sexo:
            practitioner.gender = self.codigo_sexo.lower()

        if self.data_nascimento:
            practitioner.birthDate = self.data_nascimento

        endereco = self.create_address()
        
        if not is_address_empty(endereco):
            practitioner.address=[]
            practitioner.address.append(endereco)

        if self.telefone:
            telecom = ContactPoint(
                system="phone",
                value=self.telefone,
                use="mobile"
            )
            practitioner.telecom.append(telecom)

        return practitioner
    
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

export = is_address_empty, PractitionerResource