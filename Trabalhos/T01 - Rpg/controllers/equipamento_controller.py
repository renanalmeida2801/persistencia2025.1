# controllers/equipamento_controller.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from models.equipamento import Equipamento
from services.csv_service import carregar_csv, salvar_csv
from services.zip_service import compactar_csv_para_zip
from services.xml_service import csv_para_xml
from utils.logger import log_endpoint
import os
import hashlib
from typing import List

router = APIRouter(prefix="/equipamento")
CSV_EQUIPAMENTO = "data/equipamento.csv"

def calcular_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@router.post("", response_model=Equipamento)
@log_endpoint("POST /equipamento")
def criar_equipamento(equipamento: Equipamento):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    if any(e.id == equipamento.id for e in dados):
        raise HTTPException(status_code=400, detail="ID já existe")
    dados.append(equipamento)
    salvar_csv(CSV_EQUIPAMENTO, dados, list(equipamento.dict().keys()))
    return equipamento

@router.get("", response_model=List[Equipamento])
@log_endpoint("GET /equipamento")
def listar_equipamentos():
    return carregar_csv(CSV_EQUIPAMENTO, Equipamento)

@router.put("/{equipamento_id}", response_model=Equipamento)
@log_endpoint("PUT /equipamento")
def atualizar_equipamento(equipamento_id: int, atualizado: Equipamento):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    for i, e in enumerate(dados):
        if e.id == equipamento_id:
            dados[i] = atualizado
            salvar_csv(CSV_EQUIPAMENTO, dados, list(atualizado.dict().keys()))
            return atualizado
    raise HTTPException(status_code=404, detail="Equipamento não encontrado")

@router.delete("/{equipamento_id}")
@log_endpoint("DELETE /equipamento")
def deletar_equipamento(equipamento_id: int):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    novos = [e for e in dados if e.id != equipamento_id]
    if len(novos) == len(dados):
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    salvar_csv(CSV_EQUIPAMENTO, novos, list(dados[0].dict().keys()) if novos else ["id", "nome", "tipo", "ataque", "defesa"])
    return {"mensagem": "Equipamento removido com sucesso"}

@router.get("/quantidade")
@log_endpoint("GET /equipamento/quantidade")
def contar_equipamentos():
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    return {"quantidade": len(dados)}

@router.get("/zip")
@log_endpoint("GET /equipamento/zip")
def download_equipamento_zip():
    if not os.path.exists(CSV_EQUIPAMENTO):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    zip_path = "equipamento.zip"
    compactar_csv_para_zip(CSV_EQUIPAMENTO, zip_path)
    return FileResponse(zip_path, media_type='application/zip', filename=zip_path)

@router.get("/filtrar")
@log_endpoint("GET /equipamento/filtrar")
def filtrar_equipamento(tipo: str = Query(None)):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    return [e for e in dados if tipo is None or e.tipo.lower() == tipo.lower()]

@router.get("/hash")
@log_endpoint("GET /equipamento/hash")
def hash_equipamento():
    if not os.path.exists(CSV_EQUIPAMENTO):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    return {"hash_sha256": calcular_hash(CSV_EQUIPAMENTO)}

@router.get("/xml")
@log_endpoint("GET /equipamento/xml")
def equipamento_para_xml():
    path = csv_para_xml(CSV_EQUIPAMENTO, "equipamentos", "equipamento")
    return FileResponse(path, media_type='application/xml', filename=os.path.basename(path))
