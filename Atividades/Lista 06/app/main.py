from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routers import usuarios, posts, categorias, comentarios, curtidas

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Blog Pessoal API", lifespan=lifespan)

app.include_router(usuarios.router)
app.include_router(posts.router)
app.include_router(categorias.router)
app.include_router(comentarios.router)
app.include_router(curtidas.router)