from fastapi import FastAPI

from app.models.empresa import Empresa, table_registry
from app.database import engine
from app.routers import empresas

app = FastAPI(title = "API cadastro de Empresas EcompJr")

app.include_router(empresas.router)

table_registry.metadata.create_all(engine)


@app.get('/')
def read_root():
    return {'message': 'Olá, mundo!'} 
