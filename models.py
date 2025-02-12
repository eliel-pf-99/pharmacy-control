from sqlalchemy import Column, Date, ForeignKey, Integer, String
from database import Base

class Produto(Base):
    __tablename__ = "produtos"
    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(255), nullable=False)
    sku: str = Column(String(100), nullable=False)
    barras: int = Column(String(255))
    quantidade: int = Column(Integer)
    validade: str = Column(String(100))