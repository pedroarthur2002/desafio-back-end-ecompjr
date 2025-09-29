import pytest
from fastapi.testclient import TestClient
from app.models.empresa import Empresa, table_registry
from app.app import app
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

def test_create_empresa(session):
    empresa = Empresa(
        nome='test x',
        cnpj='424141341',
        cidade='cidade x',
        ramo_atuacao='test x',
        telefone='test x',
        email_contato='teste@gmail.com'
    )

    session.add(empresa)
    session.commit()
  
    assert empresa.id == 1