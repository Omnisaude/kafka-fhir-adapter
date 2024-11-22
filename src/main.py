import logging
import os
import faust

from src.validador import is_mensagem_valida

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

broker = os.getenv('KAFKA_BROKER', 'kafka://localhost:9092')
topic_name = os.getenv('TOPIC_NAME', 'bem-vindo')

app = faust.App('consumer_faust', broker=broker)
topico_bemvindo = app.topic(topic_name)

@app.agent(topico_bemvindo)
async def consumer_faust(registros):
    async for registro in registros:
        if is_mensagem_valida(registro):
            logging.info(f"Mensagem {registro} validada com sucesso!")
        else:
            logging.error(f"Mensagem {registro} validada com falha")


if __name__ == '__main__':
    app.main()
