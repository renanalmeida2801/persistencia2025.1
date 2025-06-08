from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class CategoriaFenomeno(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    explicacao_possivel: str
    nivel_misterio: int
    popularidade: int

    relatos: List["Relato"] = Relationship(back_populates="categoria")