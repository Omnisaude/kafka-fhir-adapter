FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka_fhir_adapter ./kafka-fhir-adapter

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
