import logging
import faust
from confluent_kafka.schema_registry import SchemaRegistryClient

from kafka_fhir_adapter import config
from kafka_fhir_adapter.consumers.organization import OrganizationConsumer
from kafka_fhir_adapter.consumers.patient import PatientConsumer
from kafka_fhir_adapter.consumers.location import LocationConsumer
from kafka_fhir_adapter.consumers.encounter import EncounterConsumer
from kafka_fhir_adapter.consumers.condition import ConditionConsumer
from kafka_fhir_adapter.consumers.practitioner import PractitionerConsumer
from kafka_fhir_adapter.consumers.practitioner_role import PractitionerRoleConsumer
from kafka_fhir_adapter.consumers.surgery import SurgeryConsumer

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

app = faust.App('fhir_consumer', broker=config.KAFKA_BROKER_URL, value_serializer='raw')
schema_registry_client = SchemaRegistryClient({'url': config.SCHEMA_REGISTRY_URL})

# TOPICOS QUE SERAO CONSUMIDOS
organization_consumer = OrganizationConsumer(app, schema_registry_client, fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_ORGANIZATION_NAME)
patient_consumer = PatientConsumer(app, schema_registry_client, fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_PATIENT_NAME)
location_consumer = LocationConsumer(app, schema_registry_client, fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_LOCATION_NAME)
encounter_consumer = EncounterConsumer(app, schema_registry_client, fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_ENCOUNTER_NAME)
condition_consumer = ConditionConsumer(app,schema_registry_client,fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_CONDITION_NAME)
practitioner_consumer = PractitionerConsumer(app,schema_registry_client,fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_PRACTITIONER_NAME)
practitioner_role_consumer = PractitionerRoleConsumer(app,schema_registry_client,fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_PRACTITIONER_ROLE_NAME)
surgery_consumer = SurgeryConsumer(app,schema_registry_client,fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_SURGERY_NAME)

@app.agent(organization_consumer.topic_name)
async def process_organization_topic(messages):
    await organization_consumer.consume(messages)

@app.agent(patient_consumer.topic_name)
async def process_patient_topic(messages):
    await patient_consumer.consume(messages)

@app.agent(location_consumer.topic_name)
async def process_location_topic(messages):
    await location_consumer.consume(messages)

@app.agent(encounter_consumer.topic_name)
async def process_encounter_topic(messages):
    await encounter_consumer.consume(messages)

@app.agent(condition_consumer.topic_name)
async def process_condition_topic(messages):
    await condition_consumer.consume(messages)

@app.agent(practitioner_consumer.topic_name)
async def process_practitioner_topic(messages):
    await practitioner_consumer.consume(messages)

@app.agent(practitioner_role_consumer.topic_name)
async def process_practitioner_role_topic(messages):
    await practitioner_role_consumer.consume(messages)

@app.agent(surgery_consumer.topic_name)
async def process_surgery_topic(messages):
    await surgery_consumer.consume(messages)

# @app.agent(topico_ginfes_nfse)
# async def process_topico_ginfes_nfse(messages):
#     async for message in messages:
#         if validate_payload(message):
#             logging.info(f"Mensagem {message} validada com sucesso!")
#         else:
#             logging.error(f"Mensagem {message} validada com falha")


if __name__ == '__main__':
    app.main()
