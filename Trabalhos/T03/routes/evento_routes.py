from fastapi import APIRouter, HTTPException, Depends, Query
from config.database import db
from models.evento import Evento
from typing import List, Optional
from datetime import datetime
from utils.pagination import get_pagination
from logger import logger

router = APIRouter()
colecao = db.eventos  # coleção no MongoDB

# Helper para remover campo _id dos documentos Mongo
def remover_id(doc):
    doc.pop("_id", None)
    return doc

@router.post("/", response_model=Evento)
async def criar_evento(evento: Evento):
    logger.info("POST /eventos - Criando novo evento")
    evento_dict = evento.dict()

    if isinstance(evento_dict["data"], datetime):
        pass  
    else:
        evento_dict["data"] = datetime.combine(evento_dict["data"], datetime.min.time())

    await colecao.insert_one(evento_dict)
    logger.info(f"Evento criado com sucesso: {evento_dict['nome']} ({evento_dict['id']})")
    return remover_id(evento_dict)

@router.get("/filtro", response_model=List[Evento])
async def filtrar_eventos(
    nome: Optional[str] = Query(None),
    categoria_id: Optional[str] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None)
):
    logger.info("GET /eventos/filtro - Filtro solicitado")
    filtro = {}

    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}  # busca parcial, case-insensitive

    if categoria_id:
        filtro["categoria_id"] = categoria_id

    if data_inicio and data_fim:
        filtro["data"] = {"$gte": data_inicio, "$lte": data_fim}
    elif data_inicio:
        filtro["data"] = {"$gte": data_inicio}
    elif data_fim:
        filtro["data"] = {"$lte": data_fim}

    print("Filtro gerado:", filtro)
    logger.info(f"Filtro aplicado: {filtro}")
    eventos = await colecao.find(filtro).to_list(1000)
    logger.info(f"Eventos encontrados: {len(eventos)}")
    return [remover_id(e) for e in eventos]


@router.get("/", response_model=List[Evento])
async def listar_eventos(
    pagination: dict = Depends(get_pagination),
    sort_by: Optional[str] = Query("data", description="Campo para ordenar"),
    order: Optional[str] = Query("asc", description="asc para crescente, desc para decrescente")
):
    from pymongo import ASCENDING, DESCENDING
    logger.info("GET /eventos - Listando eventos paginados")
    page = pagination.get("page", 1)
    limit = pagination.get("limit", 10)
    skip = (page - 1) * limit
    direcao = ASCENDING if order == "asc" else DESCENDING

    logger.info(f"Paginação: página={page}, limite={limit}, ordenação={sort_by} {order.upper()}")
    eventos = await colecao.find().sort(sort_by, direcao).skip(skip).limit(limit).to_list(length=limit)
    logger.info(f"Eventos retornados: {len(eventos)}")
    return [remover_id(e) for e in eventos]

# F3 - Obter evento por ID
@router.get("/{evento_id}", response_model=Evento)
async def obter_evento(evento_id: str):
    logger.info(f"GET /eventos/{evento_id} - Buscando evento")
    evento = await colecao.find_one({"id": evento_id})
    if not evento:
        logger.warning(f"Evento não encontrado: {evento_id}")
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    logger.info(f"Evento encontrado: {evento['nome']} ({evento_id})")
    return remover_id(evento)

# F3 - Atualizar evento
@router.put("/{evento_id}", response_model=Evento)
async def atualizar_evento(evento_id: str, evento: Evento):
    logger.info(f"PUT /eventos/{evento_id} - Atualizando evento")
    evento_dict = evento.dict()

    if isinstance(evento_dict["data"], datetime):
        pass
    else:
        evento_dict["data"] = datetime.combine(evento_dict["data"], datetime.min.time())

    resultado = await colecao.update_one({"id": evento_id}, {"$set": evento_dict})
    if resultado.modified_count == 0:
        logger.warning(f"Nenhuma modificação feita. Evento {evento_id} não encontrado.")
        raise HTTPException(status_code=404, detail="Evento não encontrado para atualizar")

    evento_atualizado = await colecao.find_one({"id": evento_id})
    logger.info(f"Evento atualizado com sucesso: {evento_id}")
    return remover_id(evento_atualizado)

# F3 - Deletar evento
@router.delete("/{evento_id}")
async def deletar_evento(evento_id: str):
    logger.info(f"DELETE /eventos/{evento_id} - Tentando excluir evento")
    resultado = await colecao.delete_one({"id": evento_id})
    if resultado.deleted_count == 0:
        logger.warning(f"Evento para exclusão não encontrado: {evento_id}")
        raise HTTPException(status_code=404, detail="Evento não encontrado para exclusão")
    logger.info(f"Evento excluído com sucesso: {evento_id}")
    return {"mensagem": "Evento excluído com sucesso"}


