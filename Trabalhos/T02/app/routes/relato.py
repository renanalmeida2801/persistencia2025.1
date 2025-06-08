from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func

from app.models.relato import Relato
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=Relato)
def criar_relato(relato: Relato, session: Session = Depends(get_session)):
    session.add(relato)
    session.commit()
    session.refresh(relato)
    return relato

@router.get("/quantidade")
def contar_relatos(session:Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(Relato)).one()
    return {"quantidade": total}

@router.get("/", response_model=List[Relato])
def listar_relatos(session: Session = Depends(get_session)):
    relatos = session.exec(select(Relato)).all()
    return relatos

@router.get("/{relato_id}", response_model=Relato)
def obter_relato(relato_id: int, session: Session = Depends(get_session)):
    relato = session.get(Relato, relato_id)
    if not relato:
        raise HTTPException(status_code=404, detail="Relato não encontrado")
    return relato

@router.put("/{relato_id}", response_model=Relato)
def atualizar_relato(relato_id: int, novos_dados: Relato, session: Session = Depends(get_session)):
    relato = session.get(Relato, relato_id)
    if not relato:
        raise HTTPException(status_code=404, detail="Relato não encontrado")
    
    for campo, valor in novos_dados.dict(exclude_unset=True).items():
        setattr(relato, campo, valor)

    session.add(relato)
    session.commit()
    session.refresh(relato)
    return relato

@router.delete("/{relato_id}")
def deletar_relato(relato_id: int, session: Session = Depends(get_session)):
    relato = session.get(Relato, relato_id)
    if not relato:
        raise HTTPException(status_code=404, detail="Relato não encontrado")
    session.delete(relato)
    session.commit()
    return {"ok": True, "mensagem": "Relato deletado com sucesso"}