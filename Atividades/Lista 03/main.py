from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import xml.etree.ElementTree as ET
import os

XML_FILE = "livros.xml"

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str

app = FastAPI()

def carregar_livros() -> List[Livro]:
    if not os.path.exists(XML_FILE):
        return []
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    livros = []
    for elem in root.findall("livro"):
        livros.append(Livro(
            id=int(elem.find("id").text),
            titulo=elem.find("titulo").text,
            autor=elem.find("autor").text,
            ano=int(elem.find("ano").text),
            genero=elem.find("genero").text
        ))
    return livros

def salvar_livros(livros: List[Livro]):
    root = ET.Element("livros")
    for livro in livros:
        elem = ET.SubElement(root, "livro")
        ET.SubElement(elem, "id").text = str(livro.id)
        ET.SubElement(elem, "titulo").text = livro.titulo
        ET.SubElement(elem, "autor").text = livro.autor
        ET.SubElement(elem, "ano").text = str(livro.ano)
        ET.SubElement(elem, "genero").text = livro.genero
    ET.ElementTree(root).write(XML_FILE, encoding="utf-8", xml_declaration=True)

@app.post("/livros")
def criar_livro(livro: Livro):
    livros = carregar_livros()
    if any(l.id == livro.id for l in livros):
        raise HTTPException(status_code=400, detail="ID já existe.")
    livros.append(livro)
    salvar_livros(livros)
    return {"mensagem": "Livro criado com sucesso"}

@app.get("/livros", response_model=List[Livro])
def listar_livros():
    return carregar_livros()

@app.get("/livros/{id}", response_model=Livro)
def buscar_livro(id: int):
    for livro in carregar_livros():
        if livro.id == id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.put("/livros/{id}")
def atualizar_livro(id: int, livro_atualizado: Livro):
    livros = carregar_livros()
    for i, livro in enumerate(livros):
        if livro.id == id:
            livros[i] = livro_atualizado
            salvar_livros(livros)
            return {"mensagem": "Livro atualizado com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.delete("/livros/{id}")
def deletar_livro(id: int):
    livros = carregar_livros()
    novos = [livro for livro in livros if livro.id != id]
    if len(novos) == len(livros):
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    salvar_livros(novos)
    return {"mensagem": "Livro deletado com sucesso"}
