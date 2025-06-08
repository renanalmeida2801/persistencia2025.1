from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.relato import Relato

class RegistroMultimidia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str
    url: str
    data_registro: datetime
    legenda: str

    relato_id: Optional[int] = Field(default=None, foreign_key="relato.id")
    relato: Optional[Relato] = Relationship(back_populates="registros")