from time import perf_counter
from fastapi import status
from sqlalchemy import null
from sqlalchemy import Column
from order_router import pedidos
from sqlalchemy import create_engine, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
# pyrefly: ignore [missing-import]
from sqlalchemy_utils import ChoiceType



db = create_engine("sqlite:///banco.db")

# criar a base do banco de dados
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable= False)
    email = Column("email",String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("adm", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo = True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDIDOS = (
        ("PENDENTE","PENDENTE"),
        ("CANCELADO","CANCELADO"),
        ("FINALIZADO","FINALIZADO")
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column("status", ChoiceType(choices=STATUS_PEDIDOS), nullable=False, default= "PENDENTE")
    preco = Column("preco", Float, nullable=False)
    usuarios = Column("usuario", Integer, ForeignKey("usuarios.id"))
    

    def __init__(self, usuario, status = "pendente", preco = 0.00):
        self.usuario = usuario
        self.status = status
        self.preco = preco
        

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("quantidade",Integer,primary_key=True,autoincrement=True)
    sabor = Column("sabor",String)
    tamanho = Column("tamanho",String)
    preco = Column("preco",Float)
    pedido = Column("pedido",Integer, ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco = preco
        self.pedido = pedido
# executar as criacoes dos metadados