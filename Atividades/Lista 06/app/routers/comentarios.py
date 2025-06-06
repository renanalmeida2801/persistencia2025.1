from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.comentario import Comentario
from app.schemas.cometario import ComentarioCreate, ComentarioRead

router = APIRouter(prefix="/comentarios", tags=["Comentários"])

@router.get("/", response_model=list[ComentarioRead])
def listar_comentarios(session: Session = Depends(get_session)):
    return session.exec(select(Comentario)).all()

@router.get("/{comentario_id}", response_model=ComentarioRead)
def obter_comentario(comentario_id: int, session: Session = Depends(get_session)):
    comentario = session.get(Comentario, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    return comentario

@router.post("/", response_model=ComentarioRead)
def criar_comentario(comentario: ComentarioCreate, session: Session = Depends(get_session)):
    novo = Comentario(**comentario.dict())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return novo
