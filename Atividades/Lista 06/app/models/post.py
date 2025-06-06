from sqlmodel import SQLModel, Relationship, Field
from typing import Optional, List
from datetime import datetime

class PostCategoriaLink(SQLModel, table=True):
    post_id: Optional[int] = Field(default=None, foreign_key="post.id", primary_key=True)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id", primary_key=True)

class Post(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    titulo:str
    conteudo:str
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    autor_id: int = Field(foreign_key="usuario.id")

    autor: Optional["Usuario"] = Relationship(back_populates="posts")
    categorias: List["Categoria"] = Relationship(back_populates="posts", link_model=PostCategoriaLink)
    comentarios: List["Comentario"] = Relationship(back_populates="post")
    curtidas: List["Curtida"] = Relationship(back_populates="post")