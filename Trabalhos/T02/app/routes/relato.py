from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func

from app.models.relato import Relato
from app.database import get_session
from app.utils.logger import log_info, log_error

router = APIRouter()

@router.post("/", response_model=Relato)
def criar_relato(relato: Relato, session: Session = Depends(get_session)):
    try:
        session.add(relato)
        session.commit()
        session.refresh(relato)
        log_info(f"Relato criado: {relato}")
        return relato
    except Exception as e:
        log_error(f"Erro ao criar relato: {e}")
        raise

@router.get("/filtro", response_model=List[Relato])
def filtrar_relatos(
    titulo: str = None,
    tipo_fenomeno: str = None,
    localizacao: str = None,
    session: Session = Depends(get_session)
):
    query = select(Relato)
    filtros = {}
    if titulo:
        query = query.where(Relato.titulo.contains(titulo))
        filtros["titulo"] = titulo
    if tipo_fenomeno:
        query = query.where(Relato.tipo_fenomeno.contains(tipo_fenomeno))
        filtros["tipo_fenomeno"] = tipo_fenomeno
    if localizacao:
        query = query.where(Relato.localizacao.contains(localizacao))
        filtros["localizacao"] = localizacao

    resultados = session.exec(query).all()
    log_info(f"Filtro aplicado nos relatos: {filtros} - {len(resultados)} resultados encontrados")
    return resultados

@router.get("/quantidade", response_model=dict)
def contar_relatos(session: Session = Depends(get_session)):
    try:
        quantidade = len(session.exec(select(Relato)).all())
        log_info(f"Quantidade de relatos: {quantidade}")
        return {"quantidade": quantidade}
    except Exception as e:
        log_error(f"Erro ao contar relatos: {e}")
        raise

@router.get("/", response_model=List[Relato])
def listar_relatos_paginado(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    try:
        offset = (page - 1) * limit
        relatos = session.exec(select(Relato).offset(offset).limit(limit)).all()
        log_info(f"Listagem de relatos: página {page}, limite {limit}")
        return relatos
    except Exception as e:
        log_error(f"Erro ao listar relatos: {e}")
        raise

@router.get("/{relato_id}", response_model=Relato)
def obter_relato(relato_id: int, session: Session = Depends(get_session)):
    relato = session.get(Relato, relato_id)
    if not relato:
        log_error(f"Relato com ID {relato_id} não encontrado")
        raise HTTPException(status_code=404, detail="Relato não encontrado")
    log_info(f"Relato obtido: {relato}")
    return relato

@router.put("/{relato_id}", response_model=Relato)
def atualizar_relato(relato_id: int, novos_dados: Relato, session: Session = Depends(get_session)):
    relato = session.get(Relato, relato_id)
    if not relato:
        log_error(f"Tentativa de atualizar relato inexistente ID {relato_id}")
        raise HTTPException(status_code=404, detail="Relato não encontrado")
    
    for campo, valor in novos_dados.dict(exclude_unset=True).items():
        setattr(relato, campo, valor)

    session.add(relato)
    session.commit()
    session.refresh(relato)
    log_info(f"Relato atualizado: {relato}")
    return relato

@router.delete("/{relato_id}")
def deletar_relato(relato_id: int, session: Session = Depends(get_session)):
    relato = session.get(Relato, relato_id)
    if not relato:
        log_error(f"Tentativa de deletar relato inexistente ID {relato_id}")
        raise HTTPException(status_code=404, detail="Relato não encontrado")
    session.delete(relato)
    session.commit()
    log_info(f"Relato deletado ID: {relato_id}")
    return {"ok": True, "mensagem": "Relato deletado com sucesso"}