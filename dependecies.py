from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker, Session
from models import db

SessionLocal = sessionmaker(bind=db)

def pegar_sessao():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
