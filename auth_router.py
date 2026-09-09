from main import bcrypt_context
from idna.uts46data import uts46_statuses
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from sqlalchemy.orm import sessionmaker 
from dependecies import pegar_sessao

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    """
    Essa e a rota padrao do sistema
    """
    return {"mensagem":"Voce acessou a rota de autenticacao","autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(nome:str, email: str, senha:str, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        
        raise HTTPException(status_code=400, detail="Email do usuario ja cadastrado")
        
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario =  Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem":f"usuario cadastrado com sucesso {email}"} 
    