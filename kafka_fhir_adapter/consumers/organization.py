import json
import logging
from http.client import HTTPException

from confluent_kafka.schema_registry.avro import AvroDeserializer
from faust import App
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from kafka_fhir_adapter.database.base import SessionLocal
from kafka_fhir_adapter.database.models import OrganizationModel
from kafka_fhir_adapter.resources.organization import OrganizationResource
from kafka_fhir_adapter.services.fhir import send_payload, send_validate_payload
from kafka_fhir_adapter.services.fhir_organization import get_organization_by_cnpj, update_organization_by_cnpj, \
    update_organization_by_id

logger = logging.getLogger(__name__)


class OrganizationConsumer:
    def __init__(self, app: App, schema_registry_client, fhir_server_url, topic_name):
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
                    try:
                        # Busca o registro existente
                        mapped_organization = session.query(OrganizationModel) \
                            .filter_by(cnpj=input_organization.cnpj).first()

                        if mapped_organization:
                            logger.info(f"Organization with CNPJ {mapped_organization.cnpj} found in the database.")

                            # Verifica se o registro recebido é mais recente
                            if mapped_organization.last_update_tasy < input_organization.data_atualizacao_tasy:
                                # Atualiza o registro existente por cnpj - funcionando só que como tem duplicados na base evitei por hora
                                # updated_organization_fhir = await update_organization_by_cnpj(
                                #     app=self.app,
                                #     cnpj=input_organization.cnpj,
                                #     payload_json=input_organization_fhir
                                # )

                                # Atualiza por ID
                                updated_organization_fhir = await update_organization_by_id(
                                    app=self.app,
                                    id=mapped_organization.id_fhir,
                                    payload_json=input_organization_fhir
                                )
                                mapped_organization.last_update_tasy = input_organization.data_atualizacao_tasy
                                session.commit()
                                logger.info(
                                    f"Organization with ID {updated_organization_fhir.get('id')} updated by CNPJ {mapped_organization.cnpj}.")
                            else:
                                logger.info("Ignored - the data in the database is up to date.")
                        else:
                            # Insere novo registro se não existir
                            logger.info("Organization not found, inserting new record.")
                            result = await send_payload(self.app, message=input_organization_fhir, url=send_url)
                            new_organization = OrganizationModel(
                                cnpj=input_organization.cnpj,
                                last_update_tasy=input_organization.data_atualizacao_tasy,
                                id_fhir=result.get('id')
                            )
                            session.add(new_organization)
                            session.commit()
                            logger.info(f"New organization with CNPJ {new_organization.cnpj} added.")

                    except SQLAlchemyError as e:
                        session.rollback()
                        logger.error(f"Database error during operation: {str(e)}")
                    except HTTPException as e:
                        logger.error(f"HTTP error during communication with external service: {str(e)}")
                    except Exception as e:
                        session.rollback()
                        logger.error(f"Unexpected error: {str(e)}")
            # nao passou na validacao
            else:
                logger.error(f"invalid payload {parsed_message}")
