from pydantic import BaseModel
from typing import Optional

class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Configo:
        from_attributes = False
