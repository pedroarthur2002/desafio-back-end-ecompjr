from sqlalchemy import create_engine
from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from app.models.empresa import Base

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/empresa_db"

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()
