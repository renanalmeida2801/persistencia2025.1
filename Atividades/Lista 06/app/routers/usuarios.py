from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRead

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario)).all()

@router.get("/{usuario_id}", response_model=UsuarioRead)
def obter_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/", response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    novo = Usuario(**usuario.dict())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return novo
