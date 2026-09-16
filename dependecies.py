import os
from dotenv import load_dotenv
from models import Usuario, db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("SECRETY_KEY")
ALGORITH = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES", "30"))
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login_form")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema),session: Session = Depends(pegar_sessao)):
    try:
        dict_info = jwt.decode(token,SECRET_KEY,ALGORITH)
        id_usuario = dict_info.get("sub")
    except JWTError as erro: 
        print(erro)
        raise HTTPException(status_code = 401, detail="Acesso negado, verifique a validade do token")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario não encontrado")
        
    