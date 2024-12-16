import json
import logging

from confluent_kafka.schema_registry.avro import AvroDeserializer

from kafka_fhir_adapter.resources.sinais_vitais import SinalVital
from kafka_fhir_adapter.services.fhir import send_payload, send_validate_payload

logger = logging.getLogger(__name__)


class SinalVitalConsumer:
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

            sinal_vital = SinalVital.from_dict(parsed_message)
            sinal_vital_fhir = await sinal_vital.to_fhir()  # Chamada assíncrona
            sinal_vital_json = json.loads(sinal_vital_fhir.json())

            validate_url = f"{self.fhir_server_url}/fhir/Bundle/$validate"
            send_url = f"{self.fhir_server_url}/fhir"

            validate_response = await send_validate_payload(self.app, sinal_vital_json, url=validate_url)

            if validate_response:
                logger.info(f"Mensagem {parsed_message} validada com sucesso!")

                result = await send_payload(self.app, message=sinal_vital_json, url=send_url)
                logger.info(f"Mensagem enviada com sucesso!, {result}")
            else:
                logger.error(f"Mensagem {parsed_message} validada com falha")