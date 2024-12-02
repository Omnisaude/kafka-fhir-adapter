from sqlalchemy import Column, String, Boolean, Integer

from src.models.base import Base

"""
Para fazer o update da forma como foi definido é necessário armazenar todos os dados na RDS
i.e: Update pela data de atualizacao no tasy com complementacao de dados que estejam nulos, mesmo se o registro for mais antigo.

Para gerar migration com alembic:
alembic revision --autogenerate -m "descricao"
alembic upgrade head
"""
class OrganizationModel(Base):
    __tablename__ = "organization"

    id = Column(String, primary_key=True)
    nome_principal = Column(String)
    ativo = Column(Boolean)
    cnpj = Column(String)
    nome_alternativo_1 = Column(String)
    nome_alternativo_2 = Column(String)
    telefone = Column(String)
    pais = Column(String)
    estado = Column(String)
    cidade = Column(String)
    cep = Column(String)
    bairro = Column(String)
    complemento = Column(String)
    numero = Column(String)
    logradouro = Column(String)
    tipo_logradouro = Column(String)
    cnae = Column(String)
    data_inicio = Column(String)
    data_atualizacao_tasy = Column(String)
