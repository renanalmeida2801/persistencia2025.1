from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func
from app.models.registro import RegistroMultimidia
from app.database import get_session
from app.utils.logger import log_info, log_error

router = APIRouter()

@router.post("/", response_model=RegistroMultimidia)
def criar_registro(registro: RegistroMultimidia, session:Session = Depends(get_session)):
    try:
        session.add(registro)
        session.commit()
        session.refresh(registro)
        log_info(f"Registro criado: {registro}")
        return registro
    except Exception as e:
        log_error(f"Erro ao criar registro: {e}")
        raise

@router.get("/filtro", response_model=List[RegistroMultimidia])
def filtrar_registros(
    tipo: str = None,
    legenda: str = None,
    session: Session = Depends(get_session)
):
    try:
        query = select(RegistroMultimidia)
        filtros = {}
        if tipo:
            query = query.where(RegistroMultimidia.tipo.contains(tipo))
            filtros["tipo"] = tipo
        if legenda:
            query = query.where(RegistroMultimidia.legenda.contains(legenda))
            filtros["legenda"] = legenda
        resultados = session.exec(query).all()
        log_info(f"Filtro aplicado em registros: {filtros} - {len(resultados)} resultados")
        return resultados
    except Exception as e:
        log_error(f"Erro ao filtrar registros: {e}")
        raise

@router.get("/quantidade", response_model=dict)
def contar_registros(session: Session = Depends(get_session)):
    try:
        quantidade = len(session.exec(select(RegistroMultimidia)).all())
        log_info(f"Quantidade de registros: {quantidade}")
        return {"quantidade": quantidade}
    except Exception as e:
        log_error(f"Erro ao contar registros: {e}")
        raise

@router.get("/", response_model=List[RegistroMultimidia])
def listar_registros_paginado(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    try:
        offset = (page - 1) * limit
        registros = session.exec(select(RegistroMultimidia).offset(offset).limit(limit)).all()
        log_info(f"Listagem paginada de registros: página {page}, limite {limit}")
        return registros
    except Exception as e:
        log_error(f"Erro ao listar registros paginados: {e}")
        raise

@router.get("/{registro_id}", response_model=RegistroMultimidia)
def obter_registro(registro_id: int, session: Session= Depends(get_session)):
    try:
        registro = session.get(RegistroMultimidia, registro_id)
        if not registro:
            log_error(f"Registro com ID {registro_id} não encontrado")
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        log_info(f"Registro obtido: {registro}")
        return registro
    except Exception as e:
        log_error(f"Erro ao obter registro: {e}")
        raise

@router.put("/{registro_id}", response_model=RegistroMultimidia)
def atualizar_registro(registro_id: int, novos_dados: RegistroMultimidia, session:Session=Depends(get_session)):
    try:
        registro = session.get(RegistroMultimidia, registro_id)
        if not registro:
            log_error(f"Tentativa de atualizar registro inexistente ID {registro_id}")
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        for campo, valor in novos_dados.dict(exclude_unset=True).items():
            setattr(registro, campo, valor)
        session.commit()
        session.refresh(registro)
        log_info(f"Registro atualizado: {registro}")
        return registro
    except Exception as e:
        log_error(f"Erro ao atualizar registro: {e}")
        raise

@router.delete("/{registro_id}")
def deletar_registro(registro_id: int, session: Session = Depends(get_session)):
    try:
        registro = session.get(RegistroMultimidia, registro_id)
        if not registro:
            log_error(f"Tentativa de deletar registro inexistente ID {registro_id}")
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        session.delete(registro)
        session.commit()
        log_info(f"Registro deletado ID: {registro_id}")
        return {"ok": True, "mensagem": "Registro removido com sucesso"}
    except Exception as e:
        log_error(f"Erro ao deletar registro: {e}")
        raise