import faust

from src.config.settings import (
    DATABASE_URL, KAFKA_BROKER_URL, SCHEMA_REGISTRY_URL,
    FHIR_SERVER_URL, TOPIC_ORGANIZATION_NAME
)
from src.config.logging import logger
from src.models.base import get_engine
from src.consumer.organization_consumer import OrganizationConsumer

# engine = get_engine(DATABASE_URL)

app = faust.App('fhir_consumer', broker=KAFKA_BROKER_URL, value_serializer='raw')

organization_consumer = OrganizationConsumer(app, SCHEMA_REGISTRY_URL, FHIR_SERVER_URL, TOPIC_ORGANIZATION_NAME)
organization_consumer_topic = organization_consumer.init_topic()

@app.agent(organization_consumer_topic)
async def process_organization_topic(messages):
    await organization_consumer.process_messages(messages)


# @app.agent(topico_ginfes_nfse)
# async def process_topico_ginfes_nfse(messages):
#     async for message in messages:
#         if validate_payload(message):
#             logging.info(f"Mensagem {message} validada com sucesso!")
#         else:
#             logging.error(f"Mensagem {message} validada com falha")


if __name__ == '__main__':
    app.main()
