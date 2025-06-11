from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func

from app.models.entidade import EntidadeSobrenatural
from app.database import get_session

from app.utils.logger import log_info, log_error

router = APIRouter()

@router.post("/", response_model=EntidadeSobrenatural)
def criar_entidade(entidade: EntidadeSobrenatural, session: Session = Depends(get_session)):
    try:
        session.add(entidade)
        session.commit()
        session.refresh(entidade)
        log_info(f"Entidade criada: {entidade}")
        return entidade
    except Exception as e:
        log_error(f"Erro ao criar entidade: {e}")
        raise

@router.get("/filtro", response_model=List[EntidadeSobrenatural])
def filtrar_entidades(
    nome: str = None,
    origem: str = None,
    session: Session = Depends(get_session)
):
    try:
        query = select(EntidadeSobrenatural)
        filtros = {}
        if nome:
            query = query.where(EntidadeSobrenatural.nome.contains(nome))
            filtros["nome"] = nome
        if origem:
            query = query.where(EntidadeSobrenatural.origem.contains(origem))
            filtros["origem"] = origem
        resultados = session.exec(query).all()
        log_info(f"Filtro aplicado em entidades: {filtros} - {len(resultados)} resultados")
        return resultados
    except Exception as e:
        log_error(f"Erro ao filtrar entidades: {e}")
        raise

@router.get("/quantidade", response_model=dict)
def contar_entidades(session: Session = Depends(get_session)):
    try:
        quantidade = len(session.exec(select(EntidadeSobrenatural)).all())
        log_info(f"Quantidade de entidades: {quantidade}")
        return {"quantidade": quantidade}
    except Exception as e:
        log_error(f"Erro ao contar entidades: {e}")
        raise

@router.get("/", response_model=List[EntidadeSobrenatural])
def listar_entidades_paginado(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    try:
        offset = (page - 1) * limit
        entidades = session.exec(select(EntidadeSobrenatural).offset(offset).limit(limit)).all()
        log_info(f"Entidades listadas - página: {page}, limite: {limit}")
        return entidades
    except Exception as e:
        log_error(f"Erro ao listar entidades paginadas: {e}")
        raise

@router.get("/{entidade_id}", response_model=EntidadeSobrenatural)
def obter_entidade(entidade_id: int, session: Session = Depends(get_session)):
    try:
        entidade = session.get(EntidadeSobrenatural, entidade_id)
        if not entidade:
            log_error(f"Entidade com ID {entidade_id} não encontrada")
            raise HTTPException(status_code=404, detail="Entidade não encontrada")
        log_info(f"Entidade obtida: {entidade}")
        return entidade
    except Exception as e:
        log_error(f"Erro ao obter entidade: {e}")
        raise

@router.put("/{entidade_id}", response_model=EntidadeSobrenatural)
def atualizar_entidade(entidade_id: int, dados: EntidadeSobrenatural, session: Session = Depends(get_session)):
    try:
        entidade = session.get(EntidadeSobrenatural, entidade_id)
        if not entidade:
            log_error(f"Tentativa de atualizar entidade inexistente ID {entidade_id}")
            raise HTTPException(status_code=404, detail="Entidade não encontrada")
        for campo, valor in dados.dict(exclude_unset=True).items():
            setattr(entidade, campo, valor)
        session.commit()
        session.refresh(entidade)
        log_info(f"Entidade atualizada: {entidade}")
        return entidade
    except Exception as e:
        log_error(f"Erro ao atualizar entidade: {e}")
        raise

@router.delete("/{entidade_id}")
def deletar_entidade(entidade_id: int, session: Session = Depends(get_session)):
    try:
        entidade = session.get(EntidadeSobrenatural, entidade_id)
        if not entidade:
            log_error(f"Tentativa de deletar entidade inexistente ID {entidade_id}")
            raise HTTPException(status_code=404, detail="Entidade não encontrada")
        session.delete(entidade)
        session.commit()
        log_info(f"Entidade deletada ID: {entidade_id}")
        return {"ok": True, "mensagem": "Entidade deletada com sucesso"}
    except Exception as e:
        log_error(f"Erro ao deletar entidade: {e}")
        raise