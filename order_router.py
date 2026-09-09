import json
from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():

    """
    Essa e a rota padrao de pedidos. Todas as rotas de pedidos precisam de autenticacao
    """
    return {"mensagem":"voce acessou a ordem de pedidos"}
 