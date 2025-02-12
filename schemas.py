
import datetime
from pydantic import BaseModel
class ProdutoBase(BaseModel):
    nome: str
    sku: str 
    barras: str 
    quantidade: int
    validade: str


class ProdutoRequest(ProdutoBase):
    ...

class ProdutoResponse(ProdutoBase):
    id: int
  
    class Config:
        orm_mode = True
        from_attributes=True

class FilterRequest(BaseModel):
    de: str
    ate: str
