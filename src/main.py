import logging
import os
import faust
from confluent_kafka.serialization import SerializationError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

from dotenv import load_dotenv

from src.services.fhir import send_payload, send_validate_payload
from resources.organization import init_organization

load_dotenv()
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

broker_url = os.getenv('KAFKA_BROKER_URL', 'kafka://localhost:9092')
schema_registry_url = os.getenv('SCHEMA_REGISTRY_URL', 'http://localhost:8081')
fhir_server_url = os.getenv('FHIR_SERVER_URL', 'http://localhost:8080')

topic_organization_name = os.getenv('TOPIC_ORGANIZATION_NAME', 'organization')

app = faust.App('fhir_consumer', broker=broker_url, value_serializer='raw')
schema_registry_client = SchemaRegistryClient({'url': schema_registry_url})

# TOPICOS QUE SERAO CONSUMIDOS
organization_topic = app.topic(topic_organization_name)
# topico_organization = app.topic('origem-organization')


@app.agent(organization_topic, enable_auto_commit=False)
async def process_organization_topic(messages):
    async for raw_message in messages:
        try:
            deserializer = AvroDeserializer(schema_registry_client)
            parsed_message: dict = deserializer(raw_message, {})

            organization_fhir = init_organization(parsed_message)

            validate_response = await send_validate_payload(app, organization_fhir,
                                                            url=f'{fhir_server_url}/fhir/Organization/$validate')
            if validate_response:
                logging.info(f"Mensagem {parsed_message} validada com sucesso!")

                result = await send_payload(app, message=organization_fhir, url=f'{fhir_server_url}/fhir/Organization/')

                logging.info(f"Mensagem enviada com sucesso!, {result}")
            else:
                logging.error(f"Mensagem {parsed_message} validada com falha")

        except SerializationError as e:
            logging.error('erro ao tentar deserializar os dados em avro', e)


# @app.agent(topico_ginfes_nfse)
# async def process_topico_ginfes_nfse(messages):
#     async for message in messages:
#         if validate_payload(message):
#             logging.info(f"Mensagem {message} validada com sucesso!")
#         else:
#             logging.error(f"Mensagem {message} validada com falha")


if __name__ == '__main__':
    app.main()
