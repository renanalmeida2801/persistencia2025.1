from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func
from app.models.testemunha import Testemunha
from app.database import get_session
from app.utils.logger import log_info, log_error

router = APIRouter()

@router.post("/", response_model=Testemunha)
def criar_testemunha(testemunha: Testemunha, session: Session = Depends(get_session)):
    try:
        session.add(testemunha)
        session.commit()
        session.refresh(testemunha)
        log_info(f"Testemunha criada: {testemunha}")
        return testemunha
    except Exception as e:
        log_error(f"Erro ao criar testemunha: {e}")
        raise

@router.get("/filtro", response_model=List[Testemunha])
def filtrar_testemunhas(
    nome: str = None,
    tipo_relacao: str = None,
    experiencia_prévia: bool = None,
    session: Session = Depends(get_session)
):
    try:
        query = select(Testemunha)
        filtros = {}
        if nome:
            query = query.where(Testemunha.nome.contains(nome))
            filtros["nome"] = nome
        if tipo_relacao:
            query = query.where(Testemunha.tipo_relacao.contains(tipo_relacao))
            filtros["tipo_relacao"] = tipo_relacao
        if experiencia_prévia is not None:
            query = query.where(Testemunha.experiencia_prévia == experiencia_prévia)
            filtros["experiencia_prévia"] = experiencia_prévia
        resultados = session.exec(query).all()
        log_info(f"Filtro aplicado em testemunhas: {filtros} - {len(resultados)} resultados")
        return resultados
    except Exception as e:
        log_error(f"Erro ao filtrar testemunhas: {e}")
        raise

@router.get("/quantidade", response_model=dict)
def contar_testemunhas(session: Session = Depends(get_session)):
    try:
        quantidade = len(session.exec(select(Testemunha)).all())
        log_info(f"Quantidade de testemunhas: {quantidade}")
        return {"quantidade": quantidade}
    except Exception as e:
        log_error(f"Erro ao contar testemunhas: {e}")
        raise

@router.get("/", response_model=List[Testemunha])
def listar_testemunhas_paginado(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    try:
        offset = (page - 1) * limit
        testemunhas = session.exec(select(Testemunha).offset(offset).limit(limit)).all()
        log_info(f"Listagem paginada de testemunhas: página {page}, limite {limit}")
        return testemunhas
    except Exception as e:
        log_error(f"Erro ao listar testemunhas paginadas: {e}")
        raise

@router.get("/{testemunha_id}", response_model=Testemunha)
def obter_testemunha(testemunha_id: int, session: Session = Depends(get_session)):
    try:
        testemunha = session.get(Testemunha, testemunha_id)
        if not testemunha:
            log_error(f"Testemunha com ID {testemunha_id} não encontrada")
            raise HTTPException(status_code=404, detail="Testemunha não encontrada")
        log_info(f"Testemunha obtida: {testemunha}")
        return testemunha
    except Exception as e:
        log_error(f"Erro ao obter testemunha: {e}")
        raise

@router.put("/{testemunha_id}", response_model=Testemunha)
def atualizar_testemunha(testemunha_id: int, novos_dados: Testemunha, session: Session = Depends(get_session)):
    try:
        testemunha = session.get(Testemunha, testemunha_id)
        if not testemunha:
            log_error(f"Tentativa de atualizar testemunha inexistente ID {testemunha_id}")
            raise HTTPException(status_code=404, detail="Testemunha não encontrada")
        for campo, valor in novos_dados.dict(exclude_unset=True).items():
            setattr(testemunha, campo, valor)
        session.commit()
        session.refresh(testemunha)
        log_info(f"Testemunha atualizada: {testemunha}")
        return testemunha
    except Exception as e:
        log_error(f"Erro ao atualizar testemunha: {e}")
        raise

@router.delete("/{testemunha_id}")
def deletar_testemunha(testemunha_id: int, session: Session = Depends(get_session)):
    try:
        testemunha = session.get(Testemunha, testemunha_id)
        if not testemunha:
            log_error(f"Tentativa de deletar testemunha inexistente ID {testemunha_id}")
            raise HTTPException(status_code=404, detail="Testemunha não encontrada")
        session.delete(testemunha)
        session.commit()
        log_info(f"Testemunha deletada ID: {testemunha_id}")
        return {"ok": True, "mensagem":"Testemunha removida com sucesso"}
    except Exception as e:
        log_error(f"Erro ao deletar testemunha: {e}")
        raise