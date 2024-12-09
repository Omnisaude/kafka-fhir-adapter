from sqlalchemy import Column, String, DateTime

from kafka_fhir_adapter.database.base import Base


class OrganizationModel(Base):
    __tablename__ = 'organization_fhir'

    cnpj = Column(String, primary_key=True)
    id_fhir = Column(String, nullable=True)
    last_update_tasy = Column(DateTime(timezone=True), nullable=False)
