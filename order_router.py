from schemas import ResponsePedioSchema
from sqlalchemy import False_
from dependecies import verificar_token
from models import Usuario
from dependecies import pegar_sessao
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedioSchema
from models import Pedido, ItemPedido
from fastapi import HTTPException
from typing import List

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
    pedido.status = "CANCELADO"
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

    session.add(item_pedido)
    session.commit()
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem":"Item criado com sucesso",
        "item_pedido":item_pedido.id,
        "preco_pedido":pedido.preco
    }
    
@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, 
                   session: Session = Depends(pegar_sessao),
                   usuario: Usuario = Depends(verificar_token)):
    # Busca o item do pedido
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item do Pedido nao existente")

    # Busca o pedido associado
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido associado nao encontrado")

    # Verificação de autorização
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorização")

    # Remove o item e recalcula o preço do pedido
    session.delete(item_pedido)
    session.commit()
    pedido.calcular_preco()
    session.commit()

    return {
        "mensagem": "Item removido com sucesso",
        "item_pedido": id_item_pedido,
        "preco_pedido": pedido.preco
    }



@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido:int, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem":f"Pedido numero {pedido.id} finalizado  com sucesso",
        "pedido":pedido
    }

@order_router.get("/pedido/{id_pedido}" )
async def vizualizar_pedido(id_pedido:int, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
     pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
     if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
     if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
     return {
        "quantidade_itens_pedidos":len(pedido.itens),
         "pedido": pedido
      }
     

@order_router.get("/listar/pedido-usuario", response_model=List[ResponsePedioSchema])
async def listar_pedido(session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
   pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
   return pedidos