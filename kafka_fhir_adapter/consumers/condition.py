import json
import logging

from confluent_kafka.schema_registry.avro import AvroDeserializer

from kafka_fhir_adapter.resources.condition import ConditionResource
from kafka_fhir_adapter.services.fhir import send_payload, send_validate_payload

logger = logging.getLogger(__name__)


class ConditionConsumer:
    def __init__(self, app, schema_registry_client, fhir_server_url, topic_name):
        self.app = app
        self.schema_registry_client = schema_registry_client
        self.fhir_server_url = fhir_server_url
        self.topic_name = topic_name
        self.topic = None
        self.init_topic()

    def init_topic(self):
        if self.topic_name is None:
            self.topic = self.app.topic(self.topic_name)
        return self.topic

    async def consume(self, messages):
        async for raw_message in messages:
            deserializer = AvroDeserializer(self.schema_registry_client)
            parsed_message: dict = deserializer(raw_message, {})

            condition = ConditionResource.from_dict(parsed_message)
            condition_fhir = await condition.to_fhir()  # Chamada assíncrona
            condition_json = json.loads(condition_fhir.json())

            validate_url = f"{self.fhir_server_url}/fhir/Condition/$validate"
            send_url = f"{self.fhir_server_url}/fhir/Condition/"

            validate_response = await send_validate_payload(self.app, condition_json, url=validate_url)

            if validate_response:
                logger.info(f"Mensagem {parsed_message} validada com sucesso!")

                result = await send_payload(self.app, message=condition_json, url=send_url)
                logger.info(f"Mensagem enviada com sucesso!, {result}")
            else:
                logger.error(f"Mensagem {parsed_message} validada com falha")