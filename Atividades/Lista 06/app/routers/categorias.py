from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.categoria import Categoria
from app.models.post import PostCategoriaLink
from app.schemas.categoria import CategoriaCreate, CategoriaRead

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=list[CategoriaRead])
def listar_categorias(session: Session = Depends(get_session)):
    return session.exec(select(Categoria)).all()

@router.get("/contagem_posts", tags=["Consultas"])
def categorias_com_contagem(session: Session = Depends(get_session)):
    stmt = (
        select(Categoria, func.count(PostCategoriaLink.post_id).label("total_posts"))
        .join(PostCategoriaLink, PostCategoriaLink.categoria_id == Categoria.id)
        .group_by(Categoria.id)
        .order_by(func.count(PostCategoriaLink.post_id).desc())
    )
    results = session.exec(stmt).all()
    return [{"categoria": c, "total_posts": total} for c, total in results]

@router.get("/{categoria_id}", response_model=CategoriaRead)
def obter_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.post("/", response_model=CategoriaRead)
def criar_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    nova = Categoria(**categoria.dict())
    session.add(nova)
    session.commit()
    session.refresh(nova)
    return nova


