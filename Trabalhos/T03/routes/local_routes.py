from fastapi import APIRouter, HTTPException, Depends
from config.database import db
from models.local import Local
from typing import List
from utils.pagination import get_pagination

router = APIRouter()
colecao = db.locais

def remover_id(doc):
    doc.pop("_id", None)
    return doc

@router.post("/", response_model=Local)
async def criar_local(local: Local):
    local_dict = local.dict()
    await colecao.insert_one(local_dict)
    return remover_id(local_dict)

@router.get("/count")
async def contar_locais():
    total = await colecao.count_documents({})
    return { "total_locais": total}

@router.get("/", response_model=List[Local])
async def listar_locais(pagination: dict = Depends(get_pagination)):
    page = pagination["page"]
    limit = pagination["limit"]

    if page and limit:
        skip = (page - 1) * limit
        locais = await colecao.find().skip(skip).limit(limit).to_list(limit)
    else:
        locais = await colecao.find().to_list(1000)

    return [remover_id(l) for l in locais]

@router.get("/{local_id}", response_model=Local)
async def obter_local(local_id: str):
    local = await colecao.find_one({"id": local_id})
    if not local:
        raise HTTPException(404, "Local não encontrado")
    return remover_id(local)

@router.put("/{local_id}", response_model=Local)
async def atualizar_local(local_id: str, local: Local):
    local_dict = local.dict()
    resultado = await colecao.update_one({"id": local_id}, {"$set": local_dict})
    if resultado.modified_count == 0:
        raise HTTPException(404, "Local não encontrado para atualizar")
    local_atualizado = await colecao.find_one({"id": local_id})
    return remover_id(local_atualizado)

@router.delete("/{local_id}")
async def deletar_local(local_id: str):
    resultado = await colecao.delete_one({"id": local_id})
    if resultado.deleted_count == 0:
        raise HTTPException(404, "Local não encontrado para exclusão")
    return {"mensagem": "Local excluído com sucesso"}