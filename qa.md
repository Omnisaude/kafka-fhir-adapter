## Modo de uso
entre no terminal na pasta do projeto: docker compose up -d
o control center inicia na porta 9021
no control center vâ para dentro do cluster>tópicos e crie o topico "bem-vindo" e emita uma mensagem usando a aba messages
o servico consumer vai estar ligado ouvindo o topico
entre no log desse servico para ver o consumo: docker logs -f consumer


## Kafka Básico

### create a topic
docker exec -it broker bash
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic quickstart-events 

### Produzir
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic quickstart-events

### Consumir
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic quickstart-events --from-beginning
