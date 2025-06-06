from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.post import Post, PostCategoriaLink
from app.models.comentario import Comentario
from app.schemas.post import PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[PostRead])
def listar_posts(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(Post).offset(skip).limit(limit)).all()

@router.get("/mais_comentados", tags=["Consultas"])
def posts_mais_comentados(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    stmt = (
        select(Post, func.count(Comentario.id).label("total_comentarios"))
        .join(Comentario, Comentario.post_id == Post.id)
        .group_by(Post.id)
        .order_by(func.count(Comentario.id).desc())
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(stmt).all()
    return [{"post": p, "total_comentarios": total} for p, total in results]

@router.get("/buscar", response_model=list[PostRead], tags=["Filtros"])
def buscar_posts(
    palavra: str = Query(None),
    categoria_id: int = Query(None),
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    stmt = select(Post)
    if palavra:
        stmt = stmt.where(
            Post.titulo.contains(palavra) | Post.conteudo.contains(palavra)
        )
    if categoria_id:
        stmt = stmt.join(PostCategoriaLink).where(PostCategoriaLink.categoria_id == categoria_id)

    stmt = stmt.offset(skip).limit(limit)
    return session.exec(stmt).all()

@router.get("/{post_id}", response_model=PostRead)
def obter_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    return post

@router.post("/", response_model=PostRead)
def criar_post(post: PostCreate, session: Session = Depends(get_session)):
    novo = Post(**post.dict(exclude_unset=True))
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return novo

