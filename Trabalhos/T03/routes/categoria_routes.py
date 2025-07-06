from fastapi import APIRouter, HTTPException, Depends
from config.database import db
from models.categoria import Categoria
from typing import List
from utils.pagination import get_pagination

router = APIRouter()
colecao = db.categorias

def remover_id(doc):
    doc.pop("_id", None)
    return doc

@router.post("/", response_model=Categoria)
async def criar_categoria(categoria: Categoria):
    categoria_dict = categoria.dict()
    await colecao.insert_one(categoria_dict)
    return remover_id(categoria_dict)

@router.get("/count")
async def contar_categorias():
    total = await colecao.count_documents({})
    return { "total_categorias": total}

@router.get("/", response_model=List[Categoria])
async def listar_categorias(pagination: dict = Depends(get_pagination)):
    page = pagination["page"]
    limit = pagination["limit"]

    if page and limit:
        skip = (page - 1) * limit
        categorias = await colecao.find().skip(skip).limit(limit).to_list(limit)
    else:
        categorias = await colecao.find().to_list(1000)

    return [remover_id(c) for c in categorias]

@router.get("/{categoria_id}", response_model=Categoria)
async def obter_categoria(categoria_id: str):
    categoria = await colecao.find_one({"id": categoria_id})
    if not categoria:
        raise HTTPException(404, "Categoria não encontrada")
    return remover_id(categoria)

@router.put("/{categoria_id}", response_model=Categoria)
async def atualizar_categoria(categoria_id:str, categoria: Categoria):
    categoria_dict = categoria.dict()
    resultado = await colecao.update_one({"id": categoria_id}, {"$set": categoria_dict})
    if resultado.modified_count == 0:
        raise HTTPException(404, "Categoria não encontrada para atualizar")
    categoria_atualizada = await colecao.find_one({"id": categoria_id})
    return remover_id(categoria_atualizada)

@router.delete("/{categoria_id}")
async def deletar_categoria(categoria_id: str):
    resultado = await colecao.delete_one({"id": categoria_id})
    if resultado.deleted_count == 0:
        raise HTTPException(404, "Categoria não encontrada para exclusão")
    return {"mensagem": "Categoria excluída com sucesso"}