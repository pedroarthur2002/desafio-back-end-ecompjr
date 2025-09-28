from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    cidade = Column(String, nullable=False)
    ramo_atuacao = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email_contato = Column(String, unique=True, nullable=True)
    contato = Column(String, nullable=True)
    data_cadastro = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
