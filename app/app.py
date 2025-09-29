from http import HTTPStatus

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import EmpresaCreate
from app.models.empresa import Empresa
from app.database import get_db

app = FastAPI(title = "API cadastro de Empresas EcompJr")

@app.get('/')
def read_root():
    return {'message': 'Olá, mundo!'}

@app.post('/empresas/')
def create_firm(empresa: EmpresaCreate,  db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.model_dump())

    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa