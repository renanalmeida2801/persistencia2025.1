from fastapi import APIRouter, HTTPException, Depends, Query
from config.database import db
from models.ingresso import Ingresso
from typing import List, Optional
from datetime import datetime, date
from utils.pagination import get_pagination
from logger import logger

router = APIRouter()
colecao = db.ingressos

def remover_id(doc):
    doc.pop("_id", None)
    return doc

def normalizar_datas(ingresso_dict):
    # Convertendo data_emissao para datetime
    if isinstance(ingresso_dict["data_emissao"], datetime) is False:
        ingresso_dict["data_emissao"] = datetime.combine(ingresso_dict["data_emissao"], datetime.min.time())
    # Convertendo evento.data para datetime
    if isinstance(ingresso_dict["evento"]["data"], datetime) is False:
        ingresso_dict["evento"]["data"] = datetime.combine(ingresso_dict["evento"]["data"], datetime.min.time())
    return ingresso_dict

@router.post("/", response_model=Ingresso)
async def criar_ingresso(ingresso: Ingresso):
    ingresso_dict = ingresso.dict()

    if isinstance(ingresso_dict["data_emissao"], datetime):
        pass
    else:
        ingresso_dict["data_emissao"] = datetime.combine(ingresso_dict["data_emissao"], datetime.min.time())

    await colecao.insert_one(ingresso_dict)
    logger.info(f"Ingresso criado: {ingresso_dict['id']}") 
    return remover_id(ingresso_dict)

@router.get("/filtro", response_model=List[Ingresso])
async def filtrar_ingressos(
    preco_min: Optional[float] = Query(None),
    preco_max: Optional[float] = Query(None),
    data_emissao: Optional[date] = Query(None)
):
    filtro = {}

    if preco_min is not None or preco_max is not None:
        filtro["preco"] = {}
        if preco_min is not None:
            filtro["preco"]["$gte"] = preco_min
        if preco_max is not None:
            filtro["preco"]["$lte"] = preco_max

    if data_emissao is not None:
        filtro["data_emissao"] = datetime.combine(data_emissao, datetime.min.time())

    ingressos = await colecao.find(filtro).to_list(100)
    logger.info(f"Consulta de ingressos com filtro: {filtro}")
    return [remover_id(i) for i in ingressos]

@router.get("/count")
async def contar_ingressos():
    total = await colecao.count_documents({})
    logger.info(f"Total de ingressos no sistema: {total}")
    return { "total_ingressos": total}

@router.get("/", response_model=List[Ingresso])
async def listar_ingressos(pagination: dict = Depends(get_pagination)):
    page = pagination["page"]
    limit = pagination["limit"]

    if page and limit:
        skip = (page - 1) * limit
        ingressos = await colecao.find().skip(skip).limit(limit).to_list(limit)
        logger.info(f"Listagem paginada de ingressos: página {page}, limite {limit}")
    else:
        ingressos = await colecao.find().to_list(1000)
        logger.info("Listagem total de ingressos (sem paginação)")
    return [remover_id(i) for i in ingressos]

@router.get("/{ingresso_id}", response_model=Ingresso)
async def obter_ingresso(ingresso_id: str):
    ingresso = await colecao.find_one({"id": ingresso_id})
    if not ingresso:
        logger.warning(f"Ingresso não encontrado: {ingresso_id}")
        raise HTTPException(404, "Ingresso não encontrado")
    logger.info(f"Ingresso recuperado: {ingresso_id}")
    return remover_id(ingresso)

@router.put("/{ingresso_id}", response_model=Ingresso)
async def atualizar_ingresso(ingresso_id: str, ingresso: Ingresso):
    ingresso_dict = ingresso.dict()
    ingresso_dict = normalizar_datas(ingresso_dict)
    resultado = await colecao.update_one({"id": ingresso_id}, {"$set": ingresso_dict})
    if resultado.modified_count == 0:
        logger.warning(f"Ingresso não encontrado para atualização: {ingresso_id}")
        raise HTTPException(404, "Ingresso não encontrado para atualizar")
    logger.info(f"Ingresso atualizado: {ingresso_id}")
    ingresso_atualizado = await colecao.find_one({"id": ingresso_id})
    return remover_id(ingresso_atualizado)

@router.delete("/{ingresso_id}")
async def deletar_ingresso(ingresso_id: str):
    resultado = await colecao.delete_one({"id": ingresso_id})
    if resultado.deleted_count == 0:
        logger.warning(f"Ingresso não encontrado para exclusão: {ingresso_id}")
        raise HTTPException(status_code=404, detail="Ingresso não encontrado para exclusão")
    logger.info(f"Ingresso excluído: {ingresso_id}")
    return {"mensagem": "Ingresso excluído com sucesso"}