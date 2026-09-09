from idna.uts46data import uts46_statuses
from fastapi import APIRouter
from models import Usuario, db
from sqlalchemy.orm import sessionmaker


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
