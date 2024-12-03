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


# from src.fhir_service import epoch_timestamp_to_iso_string, string_to_bool


def init_patient(message: dict) -> Patient:
    # Crie o paciente vazio e defina meta
    patient = Patient()
    patient.meta = Meta(
        profile=[
            "https://fhir.omnisaude.co/r4/core/StructureDefinition/paciente"
        ]
    )

    # Adiciona o nome se disponível
    if message.get('NOME_PACIENTE'):
        patient.name = [HumanName(text=message['NOME_PACIENTE'])]

    # Data de nascimento
    if message.get('DATA_NASCIMENTO'):
        patient.birthDate = message['DATA_NASCIMENTO']

    # Gênero
    if message.get('CODIGO_SEXO'):
        patient.gender = message['CODIGO_SEXO'].lower()

    # Identificadores
    identifiers = []
    if message.get('PRONTUARIO'):
        identifiers.append(Identifier(
            system="https://fhir.omnisaude.co/r4/core/sid/numero-prontuario-americas-health",
            value=message['PRONTUARIO']
        ))

    if message.get('CPF'):
        identifiers.append(Identifier(
            system="https://fhir.omnisaude.co/r4/core/sid/cpf",
            value=message['CPF']
        ))

    if message.get('CARTAO_NACIONAL_SAUDE'):
        identifiers.append(Identifier(
            system="https://fhir.omnisaude.co/r4/core/sid/cns",
            value=message['CARTAO_NACIONAL_SAUDE']
        ))

    if identifiers:
        patient.identifier = identifiers

    # Extensões
    extensions = []
    if message.get("NOME_MAE"):
        extensions.append(Extension(
            url="http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName",
            valueString=message['NOME_MAE']
        ))

    if message.get("NOME_PAI"):
        extensions.append(Extension(
            url="https://fhir.omnisaude.co/r4/core/StructureDefinition/nome-pai-paciente",
            valueString=message['NOME_PAI']
        ))

    if message.get("CODIGO_NACIONALIDADE"):
        coding_nacionalidade = Coding(
            system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRPais",
            code=message["CODIGO_NACIONALIDADE"]
        )
        codeable_concept_nacionalidade = CodeableConcept(coding=[coding_nacionalidade])
        extensions.append(Extension(
            url="http://hl7.org/fhir/StructureDefinition/patient-nationality",
            extension=[
                Extension(url="code", valueCodeableConcept=codeable_concept_nacionalidade)
            ]
        ))

    if message.get("CODIGO_RACA") or message.get("CODIGO_ETNIA"):
        extension_raca_cor_etnia = Extension(
            url="http://www.saude.gov.br/fhir/r4/StructureDefinition/BRRacaCorEtnia-1.0",
            extension=[]
        )
        
        if message.get("CODIGO_RACA"):
            coding_raca = Coding(
                system="http://www.saude.gov.br/fhir/r4/CodeSystem/BRRacaCor",
                code=message["CODIGO_RACA"]
            )
            
            codeable_concept_raca = CodeableConcept(coding=[coding_raca])
            
            extension_raca_cor_etnia.extension.append(Extension(url="race", valueCodeableConcept=codeable_concept_raca))


        if message.get("CODIGO_ETNIA"):
            coding_etnia = Coding(
                system="http://www.saude.gov.br/fhir/r4/CodeSystem/BREtniaIndigena",
                code=message["CODIGO_ETNIA"]
            )
            
            codeable_concept_etnia = CodeableConcept(coding=[coding_etnia])
            
            extension_raca_cor_etnia.extension.append(Extension(url="indigenousEthnicity", valueCodeableConcept=codeable_concept_etnia))
            
            
        extensions.append(extension_raca_cor_etnia)
            
    if extensions:
        patient.extension = extensions

    # Telefone
    if message.get("TELEFONE"):
        patient.telecom = [ContactPoint(system="phone", value=message['TELEFONE'])]
        
    endereco = create_address(message)
    
    if not is_address_empty(endereco):
        patient.address=[]
        patient.address.append(endereco)

    return patient
    

def create_address(message: dict) -> Address:
    address = Address()
    
    address_mapping = {
        "country": "CODIGO_PAIS",
        "state": "CODIGO_IBGE_ESTADO",
        "city": "CODIGO_IBGE_CIDADE",
        "postalCode": "CEP",
        "text": "ENDERECO_COMPLETO"
    }
    
    for fhir_element, message_field in address_mapping.items():
        value = message.get(message_field)
        if value is not None:
            setattr(address, fhir_element, value)
            
    # line_id, message_field
    line_mapping = {
        "tipoLogradouro": "CODIGO_TIPO_LOGRADOURO",
        "logradouro": "LOGRADOURO",
        "numero": "NUMERO",
        "complemento": "COMPLEMENTO",
        "bairro": "BAIRRO"
    }
    
    if any(message.get(message_field) is not None for message_field in line_mapping.values()):
        address.line=[]
        address.line__ext=[]
    
        for line_id, message_field in line_mapping.items():
            value = message.get(message_field)
            if value is not None:
                address.line.append(value)
                address.line__ext.append(FHIRPrimitiveExtension(id=line_id, extension=[]))
    
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


export = init_patient, create_address, is_address_empty