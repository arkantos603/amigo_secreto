from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLACHEMY_DATABASE_URL = 'sqlite:///./amigo_oculto.db'

engine = create_engine(
    SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def criar_bd():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()