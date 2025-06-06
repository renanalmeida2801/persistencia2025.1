from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.post import Post
from app.models.comentario import Comentario
from app.models.curtida import Curtida

class Usuario(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    nome:str
    email:str
    senha:str

    posts: List["Post"] = Relationship(back_populates="autor")
    comentarios: List["Comentario"] = Relationship(back_populates="autor")
    curtidas: List["Curtida"] = Relationship(back_populates="usuario")