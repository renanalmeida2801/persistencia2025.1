from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func
from app.models.entidade import EntidadeSobrenatural
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=EntidadeSobrenatural)
def criar_entidade(entidade: EntidadeSobrenatural, session: Session = Depends(get_session)):
    session.add(entidade)
    session.commit()
    session.refresh(entidade)
    return entidade

@router.get("/quantidade")
def contar_entidades(session: Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(EntidadeSobrenatural)).one()
    return {"quantidade": total}

@router.get("/", response_model=List[EntidadeSobrenatural])
def listar_entidades(session: Session = Depends(get_session)):
    return session.exec(select(EntidadeSobrenatural)).all()

@router.get("/{entidade_id}", response_model=EntidadeSobrenatural)
def obter_entidade(id: int, session: Session = Depends(get_session)):
    entidade = session.get(EntidadeSobrenatural, id)
    if not entidade:
        raise HTTPException(status_code=404, detail="Entidade não encontrada")
    return entidade

@router.put("/{entidade_id}", response_model=EntidadeSobrenatural)
def atualizar_entidade(id: int, novos_dados: EntidadeSobrenatural, session: Session = Depends(get_session)):
    entidade = session.get(EntidadeSobrenatural, id)
    if not entidade:
        raise HTTPException(status_code=404, detail="Entidade não encontrada")
    for campo, valor in novos_dados.dict(exclude_unset=True).items():
        setattr(entidade, campo, valor)
    session.commit()
    session.refresh(entidade)
    return entidade

@router.delete("/{entidade_id}")
def deletar_entidade(id: int, session: Session = Depends(get_session)):
    entidade = session.get(EntidadeSobrenatural, id)
    if not entidade:
        raise HTTPException(status_code=404, detail="Entidade não encontrada")
    session.delete(entidade)
    session.commit()
    return {"ok": True, "mensagem": "Entidade removida com sucesso"}