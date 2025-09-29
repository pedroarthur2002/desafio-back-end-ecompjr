from http import HTTPStatus

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db

from app.schemas.schemas import EmpresaCreate, EmpresaResponse
from app.models.empresa import Empresa

app = FastAPI(title = "API cadastro de Empresas EcompJr")

@app.get('/')
def read_root():
    return {'message': 'Olá, mundo!'}

@app.post('/empresas/', response_model=EmpresaResponse, status_code=HTTPStatus.CREATED)
def create_firm(empresa: EmpresaCreate, session: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.model_dump())

    session.add(db_empresa)
    session.commit()
    session.refresh(db_empresa)
    return db_empresa