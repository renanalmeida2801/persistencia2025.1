from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class EntidadeSobrenatural(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    origem: str
    periculosidade: str
    descricao: str
    aparicoes_confirmadas: int
    tipo: Optional[str] = Field(default=None) 

    relatos: List["Relato"] = Relationship(back_populates="entidade")