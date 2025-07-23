from fastapi import APIRouter, HTTPException
from config.database import db
from models.evento_artista import EventoArtista
from typing import List
from logger import logger

router = APIRouter()
colecao = db.eventos_artistas

def remover_id(doc):
    doc.pop("_id", None)
    return doc

@router.post("/", response_model=EventoArtista)
async def criar_vinculo(vinculo: EventoArtista):
    logger.info(f"Tentando criar vínculo: evento_id={vinculo.evento_id}, artista_id={vinculo.artista_id}")
    existente = await colecao.find_one({
        "evento_id": vinculo.evento_id,
        "artista_id": vinculo.artista_id
    })
    if existente:
        logger.warning(f"Vínculo já existe para evento_id={vinculo.evento_id} e artista_id={vinculo.artista_id}")
        raise HTTPException(400, "Vínculo já existe")
    vinculo_dict = vinculo.dict()
    await colecao.insert_one(vinculo_dict)
    logger.info(f"Vínculo criado com sucesso: evento_id={vinculo.evento_id}, artista_id={vinculo.artista_id}")
    return remover_id(vinculo_dict)

@router.get("/count")
async def contar_vinculos():
    total = await colecao.count_documents({})
    logger.info(f"Total de vínculos: {total}")
    return { "total_vinculos": total}

@router.get("/", response_model=List[EventoArtista])
async def listar_vinculos():
    logger.info("Listando todos os vínculos evento-artista.")
    relacoes = await colecao.find().to_list(1000)
    return [remover_id(r) for r in relacoes]

@router.get("/evento/{evento_id}", response_model=List[EventoArtista])
async def listar_artistas_de_evento(evento_id: str):
    logger.info(f"Listando artistas vinculados ao evento {evento_id}")
    relacoes = await colecao.find({"evento_id": evento_id}).to_list(1000)
    return [remover_id(r) for r in relacoes]

@router.get("/artista/{artista_id}", response_model=List[EventoArtista])
async def listar_eventos_de_artista(artista_id: str):
    logger.info(f"Listando eventos vinculados ao artista {artista_id}")
    relacoes = await colecao.find({"artista_id": artista_id}).to_list(1000)
    return [remover_id(r) for r in relacoes]

@router.delete("/")
async def deletar_vinculo(evento_id: str, artista_id: str):
    logger.info(f"Tentando remover vínculo: evento_id={evento_id}, artista_id={artista_id}")
    resultado = await colecao.delete_one({"evento_id": evento_id, "artista_id": artista_id})
    if resultado.deleted_count == 0:
        logger.warning(f"Vínculo não encontrado para remoção: evento_id={evento_id}, artista_id={artista_id}")
        raise HTTPException(404, "Vinculo não encontrado")
    logger.info(f"Vínculo removido com sucesso: evento_id={evento_id}, artista_id={artista_id}")
    return {"mensagem": "Vinculo removido com sucesso."}