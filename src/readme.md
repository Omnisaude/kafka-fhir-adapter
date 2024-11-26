## comando para dar build deste dockerfile manualmente
docker build -t meucontainer -f faust/Dockerfile .


kafka-consumer-groups --bootstrap-server broker:9092 --group fhir_consumer --describe

kafka-consumer-groups --bootstrap-server broker:9092 --group fhir_consumer --topic amh_organization --reset-offsets --to-earliest --execute
