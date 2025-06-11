from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from sqlalchemy import func

from app.models.categoria import CategoriaFenomeno
from app.database import get_session
from app.utils.logger import log_info, log_error

router = APIRouter()

@router.post("/", response_model=CategoriaFenomeno)
def criar_categoria(categoria: CategoriaFenomeno, session: Session = Depends(get_session)):
    try:
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        log_info(f"Categoria criada: {categoria}")
        return categoria
    except Exception as e:
        log_error(f"Erro ao criar categoria: {e}")
        raise

@router.get("/filtro", response_model=List[CategoriaFenomeno])
def filtrar_categorias(
    nome: Optional[str] = Query(default=None),
    explicacao_possivel: Optional[str] = Query(default=None),
    session: Session = Depends(get_session)
):
    try:
        query = select(CategoriaFenomeno)
        filtros = {}
        if nome:
            query = query.where(CategoriaFenomeno.nome.contains(nome))
            filtros["nome"] = nome
        if explicacao_possivel:
            query = query.where(CategoriaFenomeno.explicacao_possivel.contains(explicacao_possivel))
            filtros["explicacao_possivel"] = explicacao_possivel
        resultados = session.exec(query).all()
        log_info(f"Filtro aplicado em categorias: {filtros} - {len(resultados)} resultados")
        return resultados
    except Exception as e:
        log_error(f"Erro ao filtrar categorias: {e}")
        raise

@router.get("/quantidade", response_model=dict)
def contar_categorias(session: Session = Depends(get_session)):
    try:
        quantidade = len(session.exec(select(CategoriaFenomeno)).all())
        log_info(f"Quantidade de categorias: {quantidade}")
        return {"quantidade": quantidade}
    except Exception as e:
        log_error(f"Erro ao contar categorias: {e}")
        raise

@router.get("/", response_model=List[CategoriaFenomeno])
def listar_categorias_paginado(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    try:
        offset = (page - 1) * limit
        categorias = session.exec(select(CategoriaFenomeno).offset(offset).limit(limit)).all()
        log_info(f"Listagem de categorias: página {page}, limite {limit}")
        return categorias
    except Exception as e:
        log_error(f"Erro ao listar categorias: {e}")
        raise

@router.get("/{categoria_id}", response_model=CategoriaFenomeno)
def obter_categoria(categoria_id: int, session: Session = Depends(get_session)):
    try:
        categoria = session.get(CategoriaFenomeno, categoria_id)
        if not categoria:
            log_error(f"Categoria com ID {categoria_id} não encontrada")
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        log_info(f"Categoria obtida: {categoria}")
        return categoria
    except Exception as e:
        log_error(f"Erro ao obter categoria: {e}")
        raise

@router.put("/{categoria_id}", response_model=CategoriaFenomeno)
def atualizar_categoria(categoria_id: int, dados: CategoriaFenomeno, session: Session = Depends(get_session)):
    try:
        categoria = session.get(CategoriaFenomeno, categoria_id)
        if not categoria:
            log_error(f"Tentativa de atualizar categoria inexistente ID {categoria_id}")
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        for campo, valor in dados.dict(exclude_unset=True).items():
            setattr(categoria, campo, valor)
        session.commit()
        session.refresh(categoria)
        log_info(f"Categoria atualizada: {categoria}")
        return categoria
    except Exception as e:
        log_error(f"Erro ao atualizar categoria: {e}")
        raise

@router.delete("/{categoria_id}")
def deletar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    try:
        categoria = session.get(CategoriaFenomeno, categoria_id)
        if not categoria:
            log_error(f"Tentativa de deletar categoria inexistente ID {categoria_id}")
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        session.delete(categoria)
        session.commit()
        log_info(f"Categoria deletada ID: {categoria_id}")
        return {"ok": True, "mensagem": "Categoria deletada com sucesso"}
    except Exception as e:
        log_error(f"Erro ao deletar categoria: {e}")
        raise