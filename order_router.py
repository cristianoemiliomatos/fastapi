from sqlalchemy import False_
from dependecies import verificar_token
from models import Usuario
from dependecies import pegar_sessao
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, ItemPedido
from fastapi import HTTPException

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

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido:int, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    pedido.status = "Cancelado"
    session.commit()
    return {
        "mensagem":f"Pedido numero {pedido.id} cancelado com sucesso",
        "pedido":pedido
    }

@order_router.get("/listar")
async def listar_pedido(session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if usuario.admin == False:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    else:
       pedidos = session.query(Pedido).all()
    return{
        "pedidos":pedidos
    }
@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, 
                    item_pedido_schema: ItemPedidoSchema,session:Session = Depends(pegar_sessao)
                  , usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorização")
    item_pedido = ItemPedido(item_pedido_schema.sabor, item_pedido_schema.tamanho,
                             item_pedido_schema.preco, id_pedido, 
                             item_pedido_schema.quantidade)

    pedido.calcular_preco()
    session.add(item_pedido)
    session.commit()
    return {
        "mensagem":"Item criado com sucesso",
        "item_pedido":item_pedido.id,
        "preco_pedido":pedido.preco
    }
    
    