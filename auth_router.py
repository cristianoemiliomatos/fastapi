from sqlalchemy import false
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependecies import pegar_sessao, verificar_token, bcrypt_context, SECRET_KEY, ALGORITH, ACESS_TOKEN_EXPIRE_MINUTES
from models import Usuario
from passlib.context import CryptContext
from schemas import UsuarioSchemas
from schemas import LoginSchema
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_inf = {"sub":str(id_usuario), "exp":data_expiracao}
    jwt_codificado = jwt.encode(dic_inf,SECRET_KEY, ALGORITH)
    return jwt_codificado



def autenticar(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


         


@auth_router.get("/")
async def autentica_login():
    return {"mensagem": "Você acessou a rota de autenticação", "autenticado": False}


@auth_router.post("/criar_conta", status_code=status.HTTP_201_CREATED)
async def criar_conta(              
    usuario_dados: UsuarioSchemas, 
    session: Session = Depends(pegar_sessao)
):
    usuario_existente = session.query(Usuario).filter(Usuario.email == usuario_dados.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email do usuário já cadastrado no sistema"
        )
    
    senha_criptografada = bcrypt_context.hash(usuario_dados.senha)
    novo_usuario = Usuario(
        nome=usuario_dados.nome,
        email=usuario_dados.email,
        senha=senha_criptografada,
        ativo=usuario_dados.ativo if usuario_dados.ativo is not None else True,
        admin=usuario_dados.admin if usuario_dados.admin is not None else False
    )


    session.add(novo_usuario)
    session.commit()
    return {"mensagem": f"Usuário cadastrado com sucesso: {usuario_dados.email}"}



@auth_router.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="usuario não encontrado ou credenciais invalidas")
    
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
     usuario = autenticar(login_schema.email, login_schema.senha, session)
     if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
     else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }



@auth_router.get("/refresh")
async def use_refresh_toke(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return {
        "acess_token":acess_token,
        "token_type":"Bearer"
    }        
