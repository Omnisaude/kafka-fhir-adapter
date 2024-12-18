import json
import logging

from confluent_kafka.schema_registry.avro import AvroDeserializer

from kafka_fhir_adapter.resources.practitioner import PractitionerResource
from kafka_fhir_adapter.services.fhir import send_payload, send_validate_payload

logger = logging.getLogger(__name__)


class PractitionerConsumer:
    def __init__(self, app, schema_registry_client, fhir_server_url, topic_name, topic_name_error):
        self.app = app
        self.schema_registry_client = schema_registry_client
        self.fhir_server_url = fhir_server_url
        self.topic_name = topic_name
        self.topic = None
        self.init_topic()
        self.topic_name_error = topic_name_error

    def init_topic(self):
        if self.topic_name is None:
            self.topic = self.app.topic(self.topic_name)
        return self.topic

    async def consume(self, messages):
        async for raw_message in messages:
            deserializer = AvroDeserializer(self.schema_registry_client)
            parsed_message: dict = deserializer(raw_message, {})

            practitioner = PractitionerResource.from_dict(parsed_message)
            practitioner_json = json.loads(practitioner.to_fhir().json())

            validate_url = f"{self.fhir_server_url}/fhir/Practitioner/$validate"
            send_url = f"{self.fhir_server_url}/fhir/Practitioner/"

            validate_response = await send_validate_payload(self.app, practitioner_json, url=validate_url,  error_topic_name= self.topic_name_error)

            if validate_response:
                logger.info(f"Mensagem {parsed_message} validada com sucesso!")

                result = await send_payload(self.app, message=practitioner_json, url=send_url)
                logger.info(f"Mensagem enviada com sucesso!, {result}")
            else:
                logger.error(f"Mensagem {parsed_message} validada com falha")