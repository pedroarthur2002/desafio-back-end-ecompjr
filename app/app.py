from http import HTTPStatus
from fastapi import HTTPException, FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.empresa import Empresa, table_registry
from app.schemas.schemas import EmpresaCreate, EmpresaResponse
from app.models.empresa import Empresa
from app.database import get_session, engine

app = FastAPI(title = "API cadastro de Empresas EcompJr")

table_registry.metadata.create_all(engine)

@app.get('/')
def read_root():
    return {'message': 'Olá, mundo!'}


@app.post('/empresas/', response_model=EmpresaResponse, status_code=HTTPStatus.CREATED)
def create_empresa(empresa: EmpresaCreate, session = Depends(get_session)):

    db_empresa = session.scalar(
        select(Empresa).where((Empresa.cnpj == empresa.cnpj) | (Empresa.email_contato == empresa.email_contato))
    )

    if db_empresa:
        if db_empresa.cnpj == empresa.cnpj:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já há uma empresa com esse CNPJ")
        elif db_empresa.email_contato == empresa.email_contato:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já há uma empresa com esse email de contato")
    else:
        db_empresa = Empresa(**empresa.model_dump())
        session.add(db_empresa)
        session.commit()
        session.refresh(db_empresa)

    return db_empresa


@app.get('/empresas/',response_model=list[EmpresaResponse] ,status_code=HTTPStatus.OK)
def get_empresas(session: Session = Depends(get_session)):
    empresas = session.scalars(select(Empresa)).all()
    return empresas


@app.get('/empresas/{id}', response_model=EmpresaResponse, status_code=HTTPStatus.OK)
def get_empresa_by_id(id: int, session: Session = Depends(get_session)):
    db_empresa = session.scalar(select(Empresa).where(Empresa.id == id))

    if not db_empresa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há empresa com esse id")
    return db_empresa


@app.delete('/empresas/{id}', status_code=HTTPStatus.NO_CONTENT)
def delete_empresa(id: int, session: Session = Depends(get_session)):
    db_empresa = session.scalar(select(Empresa).where(Empresa.id == id))

    if not db_empresa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há empresa com esse id")
    
    session.delete(db_empresa)
    session.commit

    return
