# controllers/habilidade_controller.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from models.habilidade import Habilidade
from services.csv_service import carregar_csv, salvar_csv
from services.zip_service import compactar_csv_para_zip
from services.xml_service import csv_para_xml
from utils.logger import log_endpoint
import os
import hashlib
from typing import List

router = APIRouter(prefix="/habilidade")
CSV_HABILIDADE = "data/habilidade.csv"

def calcular_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@router.post("", response_model=Habilidade)
@log_endpoint("POST /habilidade")
def criar_habilidade(habilidade: Habilidade):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    if any(h.id == habilidade.id for h in dados):
        raise HTTPException(status_code=400, detail="ID já existe")
    dados.append(habilidade)
    salvar_csv(CSV_HABILIDADE, dados, list(habilidade.dict().keys()))
    return habilidade

@router.get("", response_model=List[Habilidade])
@log_endpoint("GET /habilidade")
def listar_habilidades():
    return carregar_csv(CSV_HABILIDADE, Habilidade)

@router.put("/{habilidade_id}", response_model=Habilidade)
@log_endpoint("PUT /habilidade")
def atualizar_habilidade(habilidade_id: int, atualizado: Habilidade):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    for i, h in enumerate(dados):
        if h.id == habilidade_id:
            dados[i] = atualizado
            salvar_csv(CSV_HABILIDADE, dados, list(atualizado.dict().keys()))
            return atualizado
    raise HTTPException(status_code=404, detail="Habilidade não encontrada")

@router.delete("/{habilidade_id}")
@log_endpoint("DELETE /habilidade")
def deletar_habilidade(habilidade_id: int):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    novos = [h for h in dados if h.id != habilidade_id]
    if len(novos) == len(dados):
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")
    salvar_csv(CSV_HABILIDADE, novos, list(dados[0].dict().keys()) if novos else ["id", "nome", "descricao", "custo_mana", "nivel_requerido"])
    return {"mensagem": "Habilidade removida com sucesso"}

@router.get("/quantidade")
@log_endpoint("GET /habilidade/quantidade")
def contar_habilidades():
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    return {"quantidade": len(dados)}

@router.get("/zip")
@log_endpoint("GET /habilidade/zip")
def download_habilidade_zip():
    if not os.path.exists(CSV_HABILIDADE):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    zip_path = "habilidade.zip"
    compactar_csv_para_zip(CSV_HABILIDADE, zip_path)
    return FileResponse(zip_path, media_type='application/zip', filename=zip_path)

@router.get("/filtrar")
@log_endpoint("GET /habilidade/filtrar")
def filtrar_habilidade(nivel_requerido: int = Query(None)):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    return [h for h in dados if nivel_requerido is None or h.nivel_requerido == nivel_requerido]

@router.get("/hash")
@log_endpoint("GET /habilidade/hash")
def hash_habilidade():
    if not os.path.exists(CSV_HABILIDADE):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    return {"hash_sha256": calcular_hash(CSV_HABILIDADE)}

@router.get("/xml")
@log_endpoint("GET /habilidade/xml")
def habilidade_para_xml():
    path = csv_para_xml(CSV_HABILIDADE, "habilidades", "habilidade")
    return FileResponse(path, media_type='application/xml', filename=os.path.basename(path))
