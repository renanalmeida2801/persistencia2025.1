from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from sqlalchemy import func
from app.models.categoria import CategoriaFenomeno
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=CategoriaFenomeno)
def criar_categoria(categoria: CategoriaFenomeno, session:Session = Depends(get_session)):
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.get("/quantidade")
def contar_categorias(session:Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(CategoriaFenomeno)).one()
    return {"quantidade": total}

@router.get("/", response_model=List[CategoriaFenomeno])
def listar_entidades(session:Session = Depends(get_session)):
    return session.exec(select(CategoriaFenomeno)).all()

@router.get("/{categoria_id}", response_model=CategoriaFenomeno)
def obter_categoria(id: int, session:Session = Depends(get_session)):
    categoria = session.get(CategoriaFenomeno, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.put("/{categoria_id}")
def atualizar_categoria(id: int, novos_dados: CategoriaFenomeno, session:Session = Depends(get_session)):
    categoria = session.get(CategoriaFenomeno, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    for campo, valor in novos_dados.dict(exclude_unset=True).items():
        setattr(categoria, campo, valor)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.delete("/{categoria_id}")
def deletar_categoria(id: int, session:Session = Depends(get_session)):
    categoria = session.get(CategoriaFenomeno, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    session.delete(categoria)
    session.commit()
    return {"ok": True, "mensagem":"Categoria removida com sucesso"}