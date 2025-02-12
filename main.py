from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from models import Produto
from database import engine, Base, get_db
from repository import ProdutoRepository
from schemas import  ProdutoRequest, ProdutoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Produtos
@app.post("/api/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create(request: ProdutoRequest, db: Session = Depends(get_db)):
    produto = ProdutoRepository.save(db, Produto(**request.dict()))
    return ProdutoResponse.from_orm(produto)

@app.get("/api/produtos", response_model=list[ProdutoResponse])
def find_all(db:Session = Depends(get_db)):
    produtos = ProdutoRepository.find_all(db)
    return [ProdutoResponse.from_orm(produto).model_dump(mode="json") for produto in produtos]

@app.get("/api/produtos/id/{id}", response_model=ProdutoResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    produto = ProdutoRepository.find_by_id(db, id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    return ProdutoResponse.from_orm(produto)

@app.get("/api/produtos/name/{name}", response_model=list[ProdutoResponse])
def find_by_name(name: str, db: Session = Depends(get_db)):
    produtos = ProdutoRepository.find_by_name(db, name)
    res = []
    if not produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    for p in produtos:
        if name in p.nome:
            res.append(p)
    return [ProdutoResponse.from_orm(produto) for produto in res]

@app.get("/api/produtos/sku/{sku}", response_model=ProdutoResponse)
def find_by_sku(sku: str, db: Session = Depends(get_db)):
    produto = ProdutoRepository.find_by_sku(db, sku)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    return ProdutoResponse.from_orm(produto)

@app.get("/api/produtos/barras/{barras}", response_model=ProdutoResponse)
def find_by_id(barras: str, db: Session = Depends(get_db)):
    produto = ProdutoRepository.find_by_barras(db, barras)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    return ProdutoResponse.from_orm(produto)

@app.delete("/api/produtos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not ProdutoRepository.exists_by_id(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    ProdutoRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/produtos/{id}", response_model=ProdutoResponse)
def update(id: int, request: ProdutoRequest, db: Session = Depends(get_db)):
    if not ProdutoRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    produto = ProdutoRepository.save(db, Produto(id=id, **request.dict()))
    return ProdutoResponse.from_orm(produto)

@app.get("/api/produtos/filter", response_model=list[ProdutoResponse])
def filter_by_date(de: str, ate: str, db: Session = Depends(get_db)):
    products = ProdutoRepository.filter_by_date(db, de, ate)
    return [ProdutoResponse.from_orm(produto) for produto in products]

@app.get("/api/produtos/search/{term}", response_model=list[ProdutoResponse])
def search(term: str, db:Session = Depends(get_db)):
    products = ProdutoRepository.search(db, term)
    return [ProdutoResponse.from_orm(produto) for produto in products]
# ==============================



