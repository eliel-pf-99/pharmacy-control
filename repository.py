import datetime
from sqlalchemy.orm import Session

from models import Produto

class ProdutoRepository:
    @staticmethod
    def find_all(db: Session) -> list[Produto]:
        return db.query(Produto).all()
    
    @staticmethod
    def save(db: Session, produto: Produto) -> Produto:
        if produto.id:
            db.merge(produto)
        else:
            db.add(produto)
        db.commit()
        return produto
    
    @staticmethod
    def find_by_id(db: Session, id: int) -> Produto:
        return db.query(Produto).filter(Produto.id == id).first()
    
    @staticmethod
    def find_by_sku(db: Session, sku: str) -> Produto:
        return db.query(Produto).filter(Produto.sku == sku).first()
    
    @staticmethod
    def find_by_barras(db: Session, barras: int) -> Produto:
        return db.query(Produto).filter(Produto.barras == barras).first()

    @staticmethod
    def find_by_name(db: Session, name: str) -> list[Produto]:
        return db.query(Produto).all()
    
    @staticmethod
    def filter_by_date(db: Session, de: str, ate: str) -> list[Produto]:
        products = db.query(Produto).all()

        def str_to_day(date: str): 
            return datetime.strptime(date, '%d-%m-%Y').date()
        
        date_de = str_to_day(de)
        date_ate = str_to_day(ate)
        
        res = []

        for product in products:
            date_product = str_to_day(product.validade)
            if date_product > date_de and date_product < date_ate:
                res.append(product)

        return res
    
    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Produto).filter(Produto.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> Produto:
        produto = db.query(Produto).filter(Produto.id == id).first()
        if produto is not None:
            db.delete(produto)
            db.commit()
