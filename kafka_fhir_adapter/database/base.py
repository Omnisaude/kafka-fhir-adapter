from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from kafka_fhir_adapter import config

Base = declarative_base()

# Criação do engine
engine = create_engine(config.DATABASE_URL, echo=True)

# Criação da sessão
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Inicializar as tabelas
def init_db():
    Base.metadata.create_all(bind=engine)
