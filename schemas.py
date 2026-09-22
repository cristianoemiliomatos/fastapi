from pydantic import BaseModel, field_validator
from typing import Optional, List

class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    id_usuario:int

    class config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class config:
        from_attributes = True
class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco: float
    
    class Config:
        from_attributes = True

class ResponsePedioSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]

    @field_validator('status', mode='before')
    @classmethod
    def converter_status(cls, v):
        if hasattr(v, 'code'):
            return v.code
        return str(v)

    class Config:
        from_attributes = True


