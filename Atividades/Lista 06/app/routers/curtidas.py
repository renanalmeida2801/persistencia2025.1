from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.curtida import Curtida
from app.schemas.curtida import CurtidaCreate, CurtidaRead

router = APIRouter(prefix="/curtidas", tags=["Curtidas"])

@router.get("/", response_model=list[CurtidaRead])
def listar_curtidas(session: Session = Depends(get_session)):
    return session.exec(select(Curtida)).all()

@router.get("/{curtida_id}", response_model=CurtidaRead)
def obter_curtida(curtida_id: int, session: Session = Depends(get_session)):
    curtida = session.get(Curtida, curtida_id)
    if not curtida:
        raise HTTPException(status_code=404, detail="Curtida não encontrada")
    return curtida

@router.post("/", response_model=CurtidaRead)
def criar_curtida(curtida: CurtidaCreate, session: Session = Depends(get_session)):
    nova = Curtida(**curtida.dict())
    session.add(nova)
    session.commit()
    session.refresh(nova)
    return nova
