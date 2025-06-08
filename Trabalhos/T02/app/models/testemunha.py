from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.relato import Relato

class Testemunha(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: str
    credibilidade: int
    tipo_relacao: str
    experiencia_previa: bool

    relato_id: Optional[int] = Field(default=None, foreign_key="relato.id")
    relato: Optional[Relato] = Relationship(back_populates="testemunhas")