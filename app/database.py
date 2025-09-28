from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.empresa import Base

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/empresa_db"

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
