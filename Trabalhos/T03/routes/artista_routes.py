from fastapi import APIRouter, HTTPException, Depends, Query
from config.database import db
from models.artista import Artista
from typing import List, Optional
from datetime import datetime
from utils.pagination import get_pagination
import re

router = APIRouter()
colecao = db.artistas

def remover_id(doc):
    doc.pop("_id", None)
    return doc

@router.post("/", response_model=Artista)
async def criar_artista(artista: Artista):
    artista_dict = artista.dict()

    if isinstance(artista_dict["data_nascimento"], datetime):
        pass
    else:
        artista_dict["data_nascimento"] = datetime.combine(artista_dict["data_nascimento"], datetime.min.time())

    await colecao.insert_one(artista_dict)
    return remover_id(artista_dict)

@router.get("/filtro", response_model=List[Artista])
async def filtrar_artistas(
    nome: Optional[str] = Query(None, description="Nome parcial do artista"),
    genero: Optional[str] = Query(None, description="Gênero artístico (música, dança, poesia, etc)")
):
    filtro = {}

    if nome:
        filtro["nome"] = {"$regex": re.escape(nome), "$options": "i"}
    
    if genero:
        filtro["genero"] = {"$regex": re.escape(genero), "$options": "i"}

    artistas = await colecao.find(filtro).to_list(100)
    return [remover_id(a) for a in artistas]

@router.get("/count")
async def contar_artistas():
    total = await colecao.count_documents({})
    return { "total_artistas": total}

@router.get("/", response_model=List[Artista])
async def listar_artistas(pagination: dict = Depends(get_pagination)):
    page = pagination["page"]
    limit = pagination["limit"]

    if page and limit:
        skip = (page - 1) * limit
        artistas = await colecao.find().skip(skip).limit(limit).to_list(limit)
    else:
        artistas = await colecao.find().to_list(1000)

    return [remover_id(a) for a in artistas]

@router.get("/{artista_id}", response_model=Artista)
async def obter_artista(artista_id: str):
    artista = await colecao.find_one({"id": artista_id})
    if not artista:
        raise HTTPException(404, "Artista não encontrado")
    return remover_id(artista)

@router.put("/{artista_id}", response_model=Artista)
async def atualizar_artista(artista_id: str, artista: Artista):
    artista_dict = artista.dict()

    if isinstance(artista_dict["data_nascimento"], datetime):
        pass
    else:
        artista_dict["data_nascimento"] = datetime.combine(artista_dict["data_nascimento"], datetime.min.time())
    
    resultado = await colecao.update_one({"id": artista_id}, {"$set": artista_dict})
    if resultado.modified_count == 0:
        raise HTTPException(404, "Artista não encontrado para atualizar")
    
    artista_atualizado = await colecao.find_one({"id": artista_id})
    return remover_id(artista_atualizado)

@router.delete("/{artista_id}")
async def deletar_artista(artista_id: str):
    resultado = await colecao.delete_one({"id": artista_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Artista não encontrado para exclusão")
    return {"mensagem": "Artista excluído com sucesso"}