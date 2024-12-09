import logging
import faust
from confluent_kafka.schema_registry import SchemaRegistryClient

from kafka_fhir_adapter import config
from kafka_fhir_adapter.consumers.organization import OrganizationConsumer
from kafka_fhir_adapter.database.base import init_db

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

app = faust.App('fhir_consumer', broker=config.KAFKA_BROKER_URL, value_serializer='raw')
schema_registry_client = SchemaRegistryClient({'url': config.SCHEMA_REGISTRY_URL})

# TOPICOS QUE SERAO CONSUMIDOS
organization_consumer = OrganizationConsumer(app, schema_registry_client, fhir_server_url=config.FHIR_SERVER_URL, topic_name=config.TOPIC_ORGANIZATION_NAME)

@app.agent(organization_consumer.topic_name)
async def process_organization_topic(messages):
    await organization_consumer.consume(messages)


# @app.agent(topico_ginfes_nfse)
# async def process_topico_ginfes_nfse(messages):
#     async for message in messages:
#         if validate_payload(message):
#             logging.info(f"Mensagem {message} validada com sucesso!")
#         else:
#             logging.error(f"Mensagem {message} validada com falha")


if __name__ == '__main__':
    init_db()
    app.main()
