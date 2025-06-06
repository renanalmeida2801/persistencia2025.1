from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List
from functools import wraps
import csv
import os
import zipfile
import hashlib
import logging
import xml.etree.ElementTree as ET

app = FastAPI()

# Log
logging.basicConfig(filename="logs_api.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def registrar_log(mensagem):
    logging.info(mensagem)

def log_endpoint(nome_funcao):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            registrar_log(f"[CHAMADA] {nome_funcao} | args={args} | kwargs={kwargs}")
            resultado = func(*args, **kwargs)
            registrar_log(f"[RESPOSTA] {nome_funcao} | retorno={resultado}")
            return resultado
        return wrapper
    return decorator

# Classes
class Personagem(BaseModel):
    id: int
    nome: str
    classe: str
    nivel: int=Field(ge=1)
    pontos_vida: int=Field(ge=0)

class Habilidade(BaseModel):
    id: int
    nome: str
    descricao: str
    custo_mana: int = Field(ge=0)
    nivel_requerido:int = Field(ge=1)

class Equipamento(BaseModel):
    id: int
    nome: str
    tipo: str
    ataque: int = Field(ge=0)
    defesa: int = Field(ge=0)

CSV_PERSONAGEM = "personagem.csv"
CSV_HABILIDADE = "habilidade.csv"
CSV_EQUIPAMENTO = "equipamento.csv"

# utilitários
def carregar_csv(path:str, model: BaseModel) -> List[BaseModel]:
    if not os.path.exists(path):
        return []
    with open(path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [model(**{k: int(v) if v.isdigit() else v for k, v in row.items()}) for row in reader]

def salvar_csv(path:str, data:List[BaseModel], fields:List[str]):
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for d in data:
            writer.writerow(d.dict())

def compactar_csv_para_zip(path:str, nome_zip:str) -> str:
    with zipfile.ZipFile(nome_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(path)
    return nome_zip

def calcular_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def csv_para_xml(csv_path, tag_raiz, tag_item):
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        raiz = ET.Element(tag_raiz)
        for linha in reader:
            item = ET.SubElement(raiz, tag_item)
            for chave, valor in linha.items():
                ET.SubElement(item, chave).text = valor
        tree = ET.ElementTree(raiz)
        xml_path = csv_path.replace(".csv", ".xml")
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        return xml_path

# Endpoints personagem

@app.post("/personagem", response_model=Personagem)
@log_endpoint("POST /personagem")
def criar_personagem(personagem: Personagem):
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    if any(p.id == personagem.id for p in dados):
        raise HTTPException(status_code=400, detail="ID já existe")
    dados.append(personagem)
    salvar_csv(CSV_PERSONAGEM, dados, list(personagem.dict().keys()))
    return personagem

@app.get("/personagem", response_model=List[Personagem])
@log_endpoint("GET /personagem")
def listar_personagens():
    return carregar_csv(CSV_PERSONAGEM, Personagem)

@app.put("/personagem/{personagem_id}", response_model=Personagem)
@log_endpoint("PUT /personagem")
def atualizar_personagem(personagem_id:int, atualizado:Personagem):
    personagens = carregar_csv(CSV_PERSONAGEM, Personagem)
    for i, p in enumerate(personagens):
        if p.id == personagem_id:
            personagens[i] = atualizado
            salvar_csv(CSV_PERSONAGEM, personagens, list(atualizado.dict().keys()))
            return atualizado
    raise HTTPException(status_code=404, detail="Personagem não encontrado!")

@app.delete("/personagem/{personagem_id}")
@log_endpoint("DELETE /personagem")
def deletar_personagem(personagem_id:int):
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    novos = [p for p in dados if p.id != personagem_id]
    if len(novos) == len(dados):
        raise HTTPException(status_code=404, detail="Personagem não encontrado!")
    salvar_csv(CSV_PERSONAGEM, novos, list(dados[0].dict().keys()) if novos else["id", "nome", "classe", "nivel", "pontos_vida"])
    return{"mensagem": "Personagem removido com sucesso"}

@app.get("/personagem/quantidade")
@log_endpoint("GET /personagem/quantidade")
def contar_personagens():
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    return {"quantidade:": len(dados)}

@app.get("/personagem/zip")
@log_endpoint("GET /personagem/zip")
def download_personagem_zip():
    if not os.path.exists(CSV_PERSONAGEM):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    zip_path = "personagem.zip"
    compactar_csv_para_zip(CSV_PERSONAGEM, zip_path)
    return FileResponse(zip_path, media_type='application/zip', filename=zip_path)

@app.get("/personagem/filtrar")  # F5: filtrar
@log_endpoint("GET /personagem/filtrar")
def filtrar_personagem(classe: str = Query(None), nivel: int = Query(None)):
    dados = carregar_csv(CSV_PERSONAGEM, Personagem)
    filtrados = [
        p for p in dados if
        (classe is None or p.classe.lower() == classe.lower()) and
        (nivel is None or p.nivel == nivel)
    ]
    return filtrados

@app.get("/personagem/hash") # F6: hash
@log_endpoint("GET /personagem/hash")
def hash_personagem():
    if not os.path.exists(CSV_PERSONAGEM):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    return {"hash_sha256": calcular_hash(CSV_PERSONAGEM)}

@app.get("/personagem/xml") # F8: XML
@log_endpoint("GET /personagem/xml")
def personagem_para_xml():
    path = csv_para_xml(CSV_PERSONAGEM, "personagens", "personagem")
    return FileResponse(path, media_type='application/xml', filename=os.path.basename(path))

# Endpoints: Habilidade

@app.post("/habilidade", response_model=Habilidade)
@log_endpoint("POST /habilidade")
def criar_habilidade(habilidade:Habilidade):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    if any(h.id == habilidade.id for h in dados):
        raise HTTPException(status_code=400, detail="ID já existe.")
    dados.append(habilidade)
    salvar_csv(CSV_HABILIDADE, dados, list(habilidade.dict().keys()))
    return habilidade

@app.get("/habilidade",response_model=List[Habilidade])
@log_endpoint("GET /habilidade")
def listar_habilidades():
    return carregar_csv(CSV_HABILIDADE, Habilidade)

@app.put("/habilidade/{habilidade_id}", response_model=Habilidade)
@log_endpoint("PUT /habilidade")
def atualizar_habilidade(habilidade_id:int, atualizado:Habilidade):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    for i, h in enumerate(dados):
        if h.id == habilidade_id:
            dados[i] = atualizado
            salvar_csv(CSV_HABILIDADE, dados, list(atualizado.dict().keys()))
            return atualizado
    raise HTTPException(status_code=404, detail="Habilidade não encontrada")

@app.delete("/habilidade/{habilidade_id}")
@log_endpoint("DELETE /habilidade")
def deletar_habilidade(habilidade_id: int):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    novos = [h for h in dados if h.id != habilidade_id]
    if len(novos) == len(dados):
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")
    salvar_csv(CSV_HABILIDADE, novos, list(dados[0].dict().keys()) if novos else ["id", "nome", "descricao", "custo_mana", "nivel_requerido"])
    return {"mensagem": "Habilidade removida com sucesso"}


@app.get("/habilidade/quantidade")
@log_endpoint("GET /habilidade/quantidade")
def contar_habilidades():
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    return {"quantidade:": len(dados)}

@app.get("/habilidade/zip")
@log_endpoint("GET /habilidade/zip")
def download_habilidade_zip():
    if not os.path.exists(CSV_HABILIDADE):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    zip_path = "habilidade.zip"
    compactar_csv_para_zip(CSV_HABILIDADE, zip_path)
    return FileResponse(zip_path, media_type='application/zip', filename=zip_path)

@app.get("/habilidade/filtrar") # F5: filtrar
@log_endpoint("GET /habilidade/filtrar")
def filtrar_habilidade(nivel_requerido: int = Query(None)):
    dados = carregar_csv(CSV_HABILIDADE, Habilidade)
    return [h for h in dados if nivel_requerido is None or h.nivel_requerido == nivel_requerido]

@app.get("/habilidade/hash") # F6: hash
@log_endpoint("GET /habilidade/hash")
def hash_habilidade():
    if not os.path.exists(CSV_HABILIDADE):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    return {"hash_sha256": calcular_hash(CSV_HABILIDADE)}

@app.get("/habilidade/xml") # F8: xml
@log_endpoint("GET /habilidade/xml")
def habilidade_para_xml():
    path = csv_para_xml(CSV_HABILIDADE, "habilidades", "habilidade")
    return FileResponse(path, media_type='application/xml', filename=os.path.basename(path))

# Endpoints: Equipamento

@app.post("/equipamento", response_model=Equipamento)
@log_endpoint("POST /equipamento")
def criar_equipamento(equipamento:Equipamento):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    if any(e.id == equipamento.id for e in dados):
        raise HTTPException(status_code=400, detail="ID já existe")
    dados.append(equipamento)
    salvar_csv(CSV_EQUIPAMENTO, dados, list(equipamento.dict().keys()))
    return equipamento

@app.get("/equipamento", response_model=List[Equipamento])
@log_endpoint("GET /equipamento")
def listar_equipamentos():
    return carregar_csv(CSV_EQUIPAMENTO, Equipamento)

@app.put("/equipamento/{equipamento_id}", response_model=Equipamento)
@log_endpoint("PUT /equipamento")
def atualizar_equipamento(equipamento_id:int, atualizado:Equipamento):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    for i, e in enumerate(dados):
        if e.id == equipamento_id:
            dados[i] = atualizado
            salvar_csv(CSV_EQUIPAMENTO, dados, list(atualizado.dict().keys()))
            return atualizado
    raise HTTPException(status_code=404, detail="Equipamento não encontrado")

@app.delete("/equipamento/{equipamento_id}")
@log_endpoint("DELETE /equipamento")
def deletar_equipamento(equipamento_id:int):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    novos = [e for e in dados if e.id != equipamento_id]
    if len(novos) == len(dados):
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    salvar_csv(CSV_EQUIPAMENTO, novos, list(dados[0].dict().keys()) if novos  else["id","nome", "tipo", "ataque", "defesa"])
    return {"mensagem": "Equipamento removido com sucesso."}

@app.get("/equipamento/quantidade")
@log_endpoint("GET /equipamento/quantidade")
def contar_equipamentos():
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    return {"quantidade:": len(dados)}

@app.get("/equipamento/zip")
@log_endpoint("GET /equipamento/zip")
def download_equipamento_zip():
    if not os.path.exists(CSV_EQUIPAMENTO):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    zip_path = "equipamento.zip"
    compactar_csv_para_zip(CSV_EQUIPAMENTO, zip_path)
    return FileResponse(zip_path, media_type='application/zip', filename=zip_path)

@app.get("/equipamento/filtrar")  # F5: filtrar
@log_endpoint("GET /equipamento/filtrar")
def filtrar_equipamento(tipo: str = Query(None)):
    dados = carregar_csv(CSV_EQUIPAMENTO, Equipamento)
    return [e for e in dados if tipo is None or e.tipo.lower() == tipo.lower()]

@app.get("/equipamento/hash") # F6: hash
@log_endpoint("GET /equipamento/hash")
def hash_equipamento():
    if not os.path.exists(CSV_EQUIPAMENTO):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    return {"hash_sha256": calcular_hash(CSV_EQUIPAMENTO)}

@app.get("/equipamento/xml") # F8: xml
@log_endpoint("GET /equipamento/xml")
def equipamento_para_xml():
    path = csv_para_xml(CSV_EQUIPAMENTO, "equipamentos", "equipamento")
    return FileResponse(path, media_type='application/xml', filename=os.path.basename(path))