from dependecies import pegar_sessao
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a lista de pedidos"}


@order_router.post("/pedidos")
async def criar_pedido(pedido_schema: PedidoSchema, session:Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario= pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem":f"pedido criado com sucesso. Id do pedido{novo_pedido.id}" }
