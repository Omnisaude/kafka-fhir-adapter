import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///demo.db')
KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'kafka://localhost:9092')
SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', 'http://localhost:8081')
FHIR_SERVER_URL = os.getenv('FHIR_SERVER_URL', 'http://localhost:8080')
FHIR_BASE_URL = f"{FHIR_SERVER_URL.rstrip('/')}/fhir"
TOPIC_ORGANIZATION_NAME = os.getenv('TOPIC_ORGANIZATION_NAME', 'organization')
TOPIC_PATIENT_NAME = os.getenv('TOPIC_PATIENT_NAME', 'patient')
TOPIC_LOCATION_NAME = os.getenv('TOPIC_LOCATION_NAME', 'location')
TOPIC_ENCOUNTER_NAME = os.getenv('TOPIC_ENCOUNTER_NAME', 'encounter')
TOPIC_CONDITION_NAME = os.getenv('TOPIC_CONDITION_NAME', 'condition')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://usuario:senha@ip:5432/database')
