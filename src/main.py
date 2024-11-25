import logging
import os
import faust

from src.fhir_service import send_payload, send_validate_payload
from src.resources.organization import init_organization

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

broker = os.getenv('KAFKA_BROKER', 'kafka://localhost:9092')
app = faust.App('fhir_consumer', broker=broker)

# topicos
topico_ginfes_nfse = app.topic('origem-aginfes_nfse')
# topico_organization = app.topic('origem-organization')


@app.agent(topico_ginfes_nfse, enable_auto_commit=False)
async def process_topico_ginfes_nfse(messages):
    async for message in messages:
        organization_fhir = init_organization(message)

        validate_response = await send_validate_payload(app, organization_fhir, url='http://172.36.0.84:8080/fhir/Organization/$validate')
        if validate_response:
            logging.info(f"Mensagem {message} validada com sucesso!")

            result = await send_payload(app, message=organization_fhir, url='http://172.36.0.84:8080/fhir/Organization/')
            logging.info(f"Mensagem enviada com sucesso!, {result}")
        else:
            logging.error(f"Mensagem {message} validada com falha")


# @app.agent(topico_ginfes_nfse)
# async def process_topico_ginfes_nfse(messages):
#     async for message in messages:
#         if validate_payload(message):
#             logging.info(f"Mensagem {message} validada com sucesso!")
#         else:
#             logging.error(f"Mensagem {message} validada com falha")


if __name__ == '__main__':
    app.main()
