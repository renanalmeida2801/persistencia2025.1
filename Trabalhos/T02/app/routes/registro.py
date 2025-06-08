from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func
from app.models.registro import RegistroMultimidia
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=RegistroMultimidia)
def criar_registro(registro: RegistroMultimidia, session:Session = Depends(get_session)):
    session.add(registro)
    session.commit()
    session.refresh(registro)
    return registro

@router.get("/quantidade")
def contar_registros(session: Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(RegistroMultimidia)).one()
    return{"quantidade": total}

@router.get("/", response_model=List[RegistroMultimidia])
def listar_registros(session:Session = Depends(get_session)):
    return session.exec(select(RegistroMultimidia)).all()

@router.get("/{registro_id}", response_model=RegistroMultimidia)
def obter_registro(id: int, session: Session= Depends(get_session)):
    registro = session.get(RegistroMultimidia, id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return registro

@router.put("/{reigstro_id}", response_model=RegistroMultimidia)
def atualizar_registro(id:int, novos_dados: RegistroMultimidia, session:Session=Depends(get_session)):
    registro = session.get(RegistroMultimidia, id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    for campo, valor in novos_dados.dict(exclude_unset=True).items():
        setattr(registro, campo, valor)
    session.commit()
    session.refresh(registro)
    return registro

@router.delete("/{registro_id}")
def deletar_registro(id: int, session: Session = Depends(get_session)):
    registro = session.get(RegistroMultimidia, id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    session.delete(registro)
    session.commit()
    return {"ok": True, "mensagem": "Registro removido com sucesso"}