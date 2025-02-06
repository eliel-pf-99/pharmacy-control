
import datetime
from pydantic import BaseModel
class ProdutoBase(BaseModel):
    nome: str
    sku: str 
    barras: int
    quantidade: int
    validade: str


class ProdutoRequest(ProdutoBase):
    ...

class ProdutoResponse(ProdutoBase):
    id: int
  
    class Config:
        orm_mode = True
        from_attributes=True

