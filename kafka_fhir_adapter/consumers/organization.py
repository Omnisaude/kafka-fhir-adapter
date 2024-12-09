import json
import logging

from confluent_kafka.schema_registry.avro import AvroDeserializer

from kafka_fhir_adapter.database.base import SessionLocal
from kafka_fhir_adapter.database.models import OrganizationModel
from kafka_fhir_adapter.resources.organization import OrganizationResource
from kafka_fhir_adapter.services.fhir import send_payload, send_validate_payload

logger = logging.getLogger(__name__)


class OrganizationConsumer:
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

            input_organization = OrganizationResource.from_dict(parsed_message)
            input_organization_fhir = json.loads(input_organization.to_fhir().json())

            validate_url = f"{self.fhir_server_url}/fhir/Organization/$validate"
            send_url = f"{self.fhir_server_url}/fhir/Organization/"

            is_valid_payload = await send_validate_payload(self.app, input_organization_fhir, url=validate_url)
            if is_valid_payload:
                logger.info(f"valid payload")

                with SessionLocal() as session:
                    existing_organization = session.query(OrganizationModel)\
                        .where(OrganizationModel.cnpj == input_organization.cnpj).first()

                    if existing_organization:
                        logger.info(f"organization with cnpj {existing_organization.cnpj} found, we'll update it")
                        if existing_organization.last_update_tasy < input_organization.data_atualizacao_tasy:
                            existing_organization.last_update_tasy = input_organization.data_atualizacao_tasy
                            session.commit()
                            logger.info('organization updated')
                        logger.info('the existing organization is most recently updated')
                    else:
                        logger.info("organization not found, we'll insert")
                        result = await send_payload(self.app, message=input_organization_fhir, url=send_url)

                        resource = OrganizationModel(
                            cnpj=input_organization.cnpj,
                            last_update_tasy=input_organization.data_atualizacao_tasy,
                            id_fhir=result.get('id')
                        )
                        session.add(resource)
                        session.commit()
                        logger.info(f"new organization with cnpj {resource.cnpj} added!")
            else:
                logger.error(f"invalid payload {parsed_message}")
