from fastapi import FastAPI
from app.database import init_db
from app.routes import relato, testemunha, entidade, categoria, registro

app = FastAPI(title="Catálogo de Lendas Urbanas")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(relato.router, prefix="/relatos", tags=["Relatos"])
app.include_router(testemunha.router, prefix="/testemunhas", tags=["Testemunhas"])
app.include_router(entidade.router, prefix="/entidades", tags=["Entidades"])
app.include_router(categoria.router, prefix="/categorias", tags=["Categorias"])
app.include_router(registro.router, prefix="/registros", tags=["Registros"])