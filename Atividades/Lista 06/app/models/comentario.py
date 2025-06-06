from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Comentario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conteudo:str
    data_criacao: datetime = Field(default_factory=datetime.utcnow)

    autor_id: int = Field(foreign_key="usuario.id")
    post_id: int = Field(foreign_key="post.id")

    autor: Optional["Usuario"] = Relationship(back_populates="comentarios")
    post: Optional["Post"] = Relationship(back_populates="comentarios")