from sqlalchemy.orm import CascadeOptions
from sqlalchemy import case
from sqlalchemy.orm import relationship
from sqlalchemy import Column, create_engine, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils import ChoiceType

db = create_engine("sqlite:///banco.db")

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("adm", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column("status", ChoiceType(choices=STATUS_PEDIDOS), nullable=False, default="PENDENTE")
    preco = Column("preco", Float, nullable=False, default=0.0)
    usuario = Column("usuario", Integer, ForeignKey("usuarios.id"))
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0.00):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        self.preco = sum(item.preco * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco = Column("preco", Float)
    pedido = Column("pedido", Integer, ForeignKey("pedidos.id"))
    quantidade = Column("quantidade", Integer, default=1)

    def __init__(self, sabor, tamanho, preco, pedido, quantidade=1):
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco = preco
        self.pedido = pedido
        self.quantidade = quantidade

