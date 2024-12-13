# Kafka Fhir Adapter

- Example project of how you can use faust_streaming to processing the streaming
and filter messages that are not suitable to proceed for forward processing.

## Variaveis de ambiente necessárias (.env ou compose.yaml)
```
#KAFKA_BROKER_URL='http://ip_do_servidor:8080'
#SCHEMA_REGISTRY_URL='http://ip_do_servidor:8080'
FHIR_SERVER_URL='http://ip_do_servidor:8080'
TOPIC_ORGANIZATION_NAME='amh_organization'
DATABASE_URL='postgresql://senha:password@ip:5432/database'
```

## Configurar debug local
- Script: ./kafka_fhir_adapter/main.py
- Passe isso no script parameters: 
``` -A kafka_fhir_adapter.main worker -l info```

## comando para dar build deste dockerfile manualmente
docker build -t meucontainer -f faust/Dockerfile .

### comandos para reiniciar o consumo do consumer-groups (para testes)
- kafka-consumer-groups --bootstrap-server broker:9092 --group fhir_consumer --describe
- kafka-consumer-groups --bootstrap-server broker:9092 --group fhir_consumer --topic amh_organization --reset-offsets --to-earliest --execute

## Testes

### Pré requisitos
Subir servidor de testes (1) e adicionar os recursos da pasta `tests/resources` (2)

Primeiramente **dentro da pasta `tests`** de permissão para os scripts
```bash
cd tests
sudo chmod +x *.sh
```

(1)  
Para subir servidor de teste rode o script `up_servidor_test.sh`

```bash
./up_servidor_test.sh
```

(2)  
Para adicionar os recursos da pasta `tests/resources` rode o script `add_resources_test.sh`

```bash
./add_resources_test.sh
```

Por fim, para executar todos os testes:

```bash
pytest
```

## Dependências
Instale as dependências usando o `pip`:

```bash
pip install -r requirements.txt
```