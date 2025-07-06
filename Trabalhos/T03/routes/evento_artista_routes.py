from fastapi import APIRouter, HTTPException
from config.database import db
from models.evento_artista import EventoArtista
from typing import List

router = APIRouter()
colecao = db.eventos_artistas

def remover_id(doc):
    doc.pop("_id", None)
    return doc

@router.post("/", response_model=EventoArtista)
async def criar_vinculo(vinculo: EventoArtista):
    existente = await colecao.find_one({
        "evento_id": vinculo.evento_id,
        "artista_id": vinculo.artista_id
    })
    if existente:
        raise HTTPException(400, "Vínculo já existe")
    vinculo_dict = vinculo.dict()
    await colecao.insert_one(vinculo_dict)
    return remover_id(vinculo_dict)

@router.get("/count")
async def contar_vinculos():
    total = await colecao.count_documents({})
    return { "total_vinculos": total}

@router.get("/", response_model=List[EventoArtista])
async def listar_vinculos():
    relacoes = await colecao.find().to_list(1000)
    return [remover_id(r) for r in relacoes]

@router.get("/evento/{evento_id}", response_model=List[EventoArtista])
async def listar_artistas_de_evento(evento_id: str):
    relacoes = await colecao.find({"evento_id": evento_id}).to_list(1000)
    return [remover_id(r) for r in relacoes]

@router.get("/artista/{artista_id}", response_model=List[EventoArtista])
async def listar_eventos_de_artista(artista_id: str):
    relacoes = await colecao.find({"artista_id": artista_id}).to_list(1000)
    return [remover_id(r) for r in relacoes]

@router.delete("/")
async def deletar_vinculo(evento_id: str, artista_id: str):
    resultado = await colecao.delete_one({"evento_id": evento_id, "artista_id": artista_id})
    if resultado.deleted_count == 0:
        raise HTTPException(404, "Vinculo não encontrado")
    return {"mensagem": "Vinculo removido com sucesso."}