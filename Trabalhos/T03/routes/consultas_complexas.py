from fastapi import APIRouter, HTTPException
from config.database import db

router = APIRouter()
eventos_collection = db.eventos
categorias_collection = db.categorias
artistas_collection = db.artistas
evento_artista_collection = db.eventos_artistas
ingressos_collection = db.ingressos
locais_collection = db.locais

@router.get("/eventos/detalhes-completos")
async def eventos_com_detalhes():
    eventos = await eventos_collection.find().to_list(100)

    resultado = []
    for evento in eventos:
        categoria = await categorias_collection.find_one({"id": evento["categoria_id"]})
        vinculacoes = await evento_artista_collection.find({"evento_id": evento["id"]}).to_list(None)
        artistas_ids = [v["artista_id"] for v in vinculacoes]
        artistas = await artistas_collection.find({"id": {"$in": artistas_ids}}).to_list(None)
        
        resultado.append({
            "evento": {
                "nome": evento["nome"],
                "descricao": evento["descricao"],
                "data": evento["data"]
            },
            "categoria": {
                "nome": categoria["nome"],
                "descricao": categoria["descricao"]
            } if categoria else None,
            "artistas": [
                {"nome": artista["nome"], "genero": artista["genero"]}
                for artista in artistas
            ]
        })
    
    return resultado

@router.get("/eventos/{evento_id}/resumo-completo")
async def evento_completo(evento_id: str):
    evento = await eventos_collection.find_one({"id": evento_id})
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    
    local = await locais_collection.find_one({"id": evento["local_id"]})
    
    ingressos = await ingressos_collection.find({"evento.nome": evento["nome"]}).to_list(None)

    vinculacoes = await evento_artista_collection.find({"evento_id": evento_id}).to_list(None)
    artistas_ids = [v["artista_id"] for v in vinculacoes]
    artistas = await artistas_collection.find({"id": {"$in": artistas_ids}}).to_list(None)

    return {
        "evento": {
            "nome": evento["nome"],
            "descricao": evento["descricao"],
            "data": evento["data"]
        },
        "local": {
            "nome": local["nome"],
            "cidade": local["cidade"]
        } if local else None,
        "ingressos": [
            {
                "preco": i["preco"],
                "disponiveis": i["disponiveis"],
                "data_emissao": i["data_emissao"]
            }
            for i in ingressos
        ],
        "artistas": [a["nome"] for a in artistas]
    }