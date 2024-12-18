import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///demo.db')
KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'kafka://localhost:9092')
SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', 'http://localhost:8081')
FHIR_SERVER_URL = os.getenv('FHIR_SERVER_URL', 'http://localhost:8080')
FHIR_BASE_URL = f"{FHIR_SERVER_URL.rstrip('/')}/fhir"
TOPIC_ORGANIZATION_NAME = os.getenv('TOPIC_ORGANIZATION_NAME', 'organization')
TOPIC_ORGANIZATION_NAME_ERROR = os.getenv('TOPIC_ORGANIZATION_NAME_ERROR', 'organization_error')

TOPIC_PATIENT_NAME = os.getenv('TOPIC_PATIENT_NAME', 'patient')
TOPIC_PATIENT_NAME_ERROR = os.getenv('TOPIC_PATIENT_NAME_ERROR', 'patient_error')

TOPIC_LOCATION_NAME = os.getenv('TOPIC_LOCATION_NAME', 'location')
TOPIC_LOCATION_NAME_ERROR = os.getenv('TOPIC_LOCATION_NAME_ERROR', 'location_error')

TOPIC_ENCOUNTER_NAME = os.getenv('TOPIC_ENCOUNTER_NAME', 'encounter')
TOPIC_ENCOUNTER_NAME_ERROR = os.getenv('TOPIC_ENCOUNTER_NAME_ERROR', 'encounter_error')

TOPIC_CONDITION_NAME = os.getenv('TOPIC_CONDITION_NAME', 'condition')
TOPIC_CONDITION_NAME_ERROR = os.getenv('TOPIC_CONDITION_NAME_ERROR', 'condition_error')

TOPIC_PRACTITIONER_NAME = os.getenv('TOPIC_PRACTITIONER_NAME', 'practitioner')
TOPIC_PRACTITIONER_NAME_ERROR = os.getenv('TOPIC_PRACTITIONER_NAME_ERROR', 'practitioner_error')

TOPIC_PRACTITIONER_ROLE_NAME = os.getenv('TOPIC_PRACTITIONER_ROLE_NAME', 'practitioner_role')
TOPIC_PRACTITIONER_ROLE_NAME_ERROR = os.getenv('TOPIC_PRACTITIONER_ROLE_NAME_ERROR', 'practitioner_role_error')

TOPIC_SURGERY_NAME = os.getenv('TOPIC_SURGERY_NAME', 'surgery')
TOPIC_SURGERY_NAME_ERROR = os.getenv('TOPIC_SURGERY_NAME_ERROR', 'surgery_error')

TOPIC_VITAL_SIGNS_NAME = os.getenv('TOPIC_VITAL_SIGNS_NAME', 'vital_signs')
TOPIC_VITAL_SIGNS_NAME_ERROR = os.getenv('TOPIC_VITAL_SIGNS_NAME_ERROR', 'vital_signs_error')