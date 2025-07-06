from fastapi import FastAPI
from routes.evento_routes import router as evento_router
from routes.local_routes import router as local_router
from routes.artista_routes import router as artista_router
from routes.categoria_routes import router as categoria_router
from routes.ingresso_routes import router as ingresso_router
from routes.evento_artista_routes import router as evento_artista_router
from routes.consultas_complexas import router as consulta_complexa_router

app = FastAPI(title="API de eventos culturais")

app.include_router(evento_router, prefix="/eventos", tags=["Eventos"])
app.include_router(local_router, prefix="/locais", tags=["Locais"])
app.include_router(artista_router, prefix="/artistas", tags=["Artistas"])
app.include_router(categoria_router, prefix="/categorias", tags=["Categorias"])
app.include_router(ingresso_router, prefix="/ingressos", tags=["Ingressos"])
app.include_router(evento_artista_router, prefix="/eventos-artistas", tags=["Vínculo Evento-Artista"])
app.include_router(consulta_complexa_router, prefix="/consultas-complexas", tags=["Consultas Complexas"])