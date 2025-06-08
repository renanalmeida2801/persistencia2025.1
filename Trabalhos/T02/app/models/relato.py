from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class Relato(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    data_ocorrencia: date
    localizacao: str
    tipo_fenomeno: str

    categoria_id: Optional[int] = Field(default=None, foreign_key="categoriafenomeno.id")
    entidade_id: Optional[int] = Field(default=None, foreign_key="entidadesobrenatural.id")

    categoria: Optional["CategoriaFenomeno"] = Relationship(back_populates="relatos")
    entidade: Optional["EntidadeSobrenatural"] = Relationship(back_populates="relatos")
    registros: List["RegistroMultimidia"] = Relationship(back_populates="relato")
    testemunhas: List["Testemunha"] = Relationship(back_populates="relato")