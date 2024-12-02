# Kafka Validator

- Example project of how you can use faust_streaming to processing the streaming
and filter messages that are not suitable to proceed for forward processing.

## Variaveis de ambiente necessárias (.env ou compose.yaml)
```
#KAFKA_BROKER_URL='http://ip_do_servidor:8080'
#SCHEMA_REGISTRY_URL='http://ip_do_servidor:8080'
FHIR_SERVER_URL='http://ip_do_servidor:8080'
TOPIC_ORGANIZATION_NAME='amh_organization'
```

## Configurar debug local
- Script: ./src/main.py
- Passe isso no script parameters: 
``` -A src.main worker -l info```
