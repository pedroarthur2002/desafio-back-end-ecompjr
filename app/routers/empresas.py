from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from app.schemas.schemas import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from app.models.empresa import Empresa
from app.database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix='/empresas', tags=['empresas'])

@router.post('/', response_model=EmpresaResponse, status_code=HTTPStatus.CREATED)
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

@router.get('/', response_model=list[EmpresaResponse], status_code=HTTPStatus.OK)
def get_empresas(
    session: Session = Depends(get_session),
    cidade: str | None = None,
    ramo_atuacao: str | None = None,
    nome: str | None = None
):
    query = select(Empresa)
    
    
    if cidade:
        query = query.where(Empresa.cidade == cidade)
    
    
    if ramo_atuacao:
        query = query.where(Empresa.ramo_atuacao == ramo_atuacao)
    
    
    if nome:
        query = query.where(Empresa.nome.ilike(f'%{nome}%'))
    
    empresas = session.scalars(query).all()
    return empresas


@router.delete('/{id}', status_code=HTTPStatus.OK)
def delete_empresa(id: int, session: Session = Depends(get_session)):
    db_empresa = session.scalar(select(Empresa).where(Empresa.id == id))

    if not db_empresa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há empresa com esse id")
    
    session.delete(db_empresa)
    session.commit()

    return {"message": "Empresa removida com sucesso"}  # Corrigido


@router.get('/{id}', response_model=EmpresaResponse, status_code=HTTPStatus.OK)
def get_empresa_by_id(id: int, session: Session = Depends(get_session)):
    db_empresa = session.scalar(select(Empresa).where(Empresa.id == id))

    if not db_empresa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há empresa com esse id")
    return db_empresa


@router.put('/{id}', response_model=EmpresaResponse, status_code=HTTPStatus.OK)
def update_empresa(id: int, empresa: EmpresaUpdate, session: Session = Depends(get_session)):
    db_empresa = session.scalar(select(Empresa).where(Empresa.id == id))

    if not db_empresa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há empresa com esse id")

    email_empresa = session.scalar(select(Empresa).where(Empresa.email_contato == empresa.email_contato, Empresa.id != id))

    if email_empresa:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma empresa com esse email")
    
    db_empresa.nome = empresa.nome
    db_empresa.cidade = empresa.cidade
    db_empresa.ramo_atuacao = empresa.ramo_atuacao
    db_empresa.telefone = empresa.telefone
    db_empresa.email_contato = empresa.email_contato

    session.commit()
    session.refresh(db_empresa)

    return db_empresa


@router.delete('/{id}', status_code=HTTPStatus.OK)
def delete_empresa(id: int, session: Session = Depends(get_session)):
    db_empresa = session.scalar(select(Empresa).where(Empresa.id == id))

    if not db_empresa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há empresa com esse id")
    
    session.delete(db_empresa)
    session.commit()

    return {"Empresa removida com sucesso"}