# controllers/personagem_controller.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from models.personagem import Personagem
from services.csv_service import carregar_csv, salvar_csv
from services.zip_service import compactar_csv_para_zip
from services.xml_service import csv_para_xml
from utils.logger import log_endpoint
import os
import hashlib
from typing import List

router = APIRouter(prefix="/personagem")
CSV_PERSONAGEM = "data/personagem.csv"

def calcular_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@router.post("", response_model=Personagem)
@log_endpoint("POST /personagem")
def criar_personagem(personagem: Personagem):
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    if any(p.id == personagem.id for p in dados):
        raise HTTPException(status_code=400, detail="ID já existe")
    dados.append(personagem)
    salvar_csv(CSV_PERSONAGEM, dados, list(personagem.dict().keys()))
    return personagem

@router.get("", response_model=List[Personagem])
@log_endpoint("GET /personagem")
def listar_personagens():
    return carregar_csv(CSV_PERSONAGEM, Personagem)

@router.put("/{personagem_id}", response_model=Personagem)
@log_endpoint("PUT /personagem")
def atualizar_personagem(personagem_id: int, atualizado: Personagem):
    personagens = carregar_csv(CSV_PERSONAGEM, Personagem)
    for i, p in enumerate(personagens):
        if p.id == personagem_id:
            personagens[i] = atualizado
            salvar_csv(CSV_PERSONAGEM, personagens, list(atualizado.dict().keys()))
            return atualizado
    raise HTTPException(status_code=404, detail="Personagem não encontrado")

@router.delete("/{personagem_id}")
@log_endpoint("DELETE /personagem")
def deletar_personagem(personagem_id: int):
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    novos = [p for p in dados if p.id != personagem_id]
    if len(novos) == len(dados):
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    salvar_csv(CSV_PERSONAGEM, novos, list(dados[0].dict().keys()) if novos else ["id", "nome", "classe", "nivel", "pontos_vida"])
    return {"mensagem": "Personagem removido com sucesso"}

@router.get("/quantidade")
@log_endpoint("GET /personagem/quantidade")
def contar_personagens():
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    return {"quantidade": len(dados)}

@router.get("/zip")
@log_endpoint("GET /personagem/zip")
def download_personagem_zip():
    if not os.path.exists(CSV_PERSONAGEM):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    zip_path = "personagem.zip"
    compactar_csv_para_zip(CSV_PERSONAGEM, zip_path)
    return FileResponse(zip_path, media_type='application/zip', filename=zip_path)

@router.get("/filtrar")
@log_endpoint("GET /personagem/filtrar")
def filtrar_personagem(classe: str = Query(None), nivel: int = Query(None)):
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    return [p for p in dados if (classe is None or p.classe.lower() == classe.lower()) and (nivel is None or p.nivel == nivel)]

@router.get("/hash")
@log_endpoint("GET /personagem/hash")
def hash_personagem():
    if not os.path.exists(CSV_PERSONAGEM):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    return {"hash_sha256": calcular_hash(CSV_PERSONAGEM)}

@router.get("/xml")
@log_endpoint("GET /personagem/xml")
def personagem_para_xml():
    path = csv_para_xml(CSV_PERSONAGEM, "personagens", "personagem")
    return FileResponse(path, media_type='application/xml', filename=os.path.basename(path))
