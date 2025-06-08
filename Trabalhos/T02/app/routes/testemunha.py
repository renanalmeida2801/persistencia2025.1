from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func
from app.models.testemunha import Testemunha
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=Testemunha)
def criar_testemunha(testemunha: Testemunha, session: Session = Depends(get_session)):
    session.add(testemunha)
    session.commit()
    session.refresh(testemunha)
    return testemunha

@router.get("/quantidades")
def contar_testemunhas(session: Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(Testemunha)).one()
    return {"quantidade": total}

@router.get("/", response_model=List[Testemunha])
def listar_testemunhas(session: Session = Depends(get_session)):
    return session.exec(select(Testemunha)).all()

@router.get("/{testemunha_id}", response_model=Testemunha)
def obter_testemunha(testemunha_id: int, session: Session = Depends(get_session)):
    testemunha = session.get(Testemunha, testemunha_id)
    if not testemunha:
        raise HTTPException(status_code=404, detail="Testemunha não encontrada")
    return testemunha

@router.put("/{testemunha_id}", response_model=Testemunha)
def atualizar_testemunha(testemunha_id: int, novos_dados: Testemunha, session: Session = Depends(get_session)):
    testemunha = session.get(Testemunha, testemunha_id)
    if not testemunha:
        raise HTTPException(status_code=404, detail="Testemunha não encontrada")
    for campo, valor in novos_dados.dict(exclude_unset=True).items():
        setattr(testemunha, campo, valor)
    session.commit()
    session.refresh(testemunha)
    return testemunha

@router.delete("/{testemunha_id}")
def deletar_testemunha(id: int, session: Session = Depends(get_session)):
    testemunha = session.get(Testemunha, id)
    if not testemunha:
        raise HTTPException(status_code=404, detail="Testemunha não encontrada")
    session.delete(testemunha)
    session.commit()
    return {"ok": True, "mensagem":"Testemunha removida com sucesso"}