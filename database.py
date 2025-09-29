from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# Caminho do banco SQLite
DATABASE_URL = "sqlite:///./empresa_db.db"

# Cria o engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criar sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Dependência para usar nas rotas FastAPI
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
