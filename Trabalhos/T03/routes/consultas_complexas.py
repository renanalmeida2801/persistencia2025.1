from fastapi import APIRouter, HTTPException
from config.database import db
from logger import logger

router = APIRouter()
eventos_collection = db.eventos
categorias_collection = db.categorias
artistas_collection = db.artistas
evento_artista_collection = db.eventos_artistas
ingressos_collection = db.ingressos
locais_collection = db.locais

@router.get("/eventos/detalhes-completos")
async def eventos_com_detalhes():
    logger.info("Iniciando consulta de eventos com detalhes completos")
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
    logger.info(f"{len(resultado)} eventos encontrados com detalhes")
    return resultado

@router.get("/eventos/{evento_id}/resumo-completo")
async def evento_completo(evento_id: str):
    logger.info(f"Buscando resumo completo para evento: {evento_id}")
    evento = await eventos_collection.find_one({"id": evento_id})
    if not evento:
        logger.warning(f"Evento {evento_id} não encontrado")
        raise HTTPException(404, "Evento não encontrado")
    
    local = await locais_collection.find_one({"id": evento["local_id"]})
    
    ingressos = await ingressos_collection.find({"evento.nome": evento["nome"]}).to_list(None)

    vinculacoes = await evento_artista_collection.find({"evento_id": evento_id}).to_list(None)
    artistas_ids = [v["artista_id"] for v in vinculacoes]
    artistas = await artistas_collection.find({"id": {"$in": artistas_ids}}).to_list(None)
    logger.info(f"Resumo do evento {evento_id} gerado com sucesso")
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

@router.get("/locais/mais-utilizados")
async def locais_mais_utilizados():
    logger.info("Iniciando agregação para encontrar locais mais utilizados")
    pipeline = [
        {
            "$group": {
                "_id": "$local_id",
                "qtd_eventos": {"$sum": 1}
            }
        },
        {
            "$sort": {"qtd_eventos": -1}
        }
    ]

    agregados = await eventos_collection.aggregate(pipeline).to_list(None)
    logger.info(f"{len(agregados)} locais agregados")

    locais_ids = [item["_id"] for item in agregados]
    locais  = await locais_collection.find({"id": {"$in": locais_ids}}).to_list(None)

    locais_dict = {local["id"]: local for local in locais}

    resultado = []

    for item in agregados:
        local_info = locais_dict.get(item["_id"])
        if local_info:
            resultado.append({
                "nome": local_info["nome"],
                "endereco": local_info.get("endereco", "N/A"),
                "cidade": local_info.get("cidade", "N/A"),
                "qtd_eventos": item["qtd_eventos"]
            })
    logger.info(f"Locais mais utilizados computados com sucesso: {len(resultado)} locais")
    return {"locais_mais_utilizados": resultado}