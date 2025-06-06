from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.post import PostCategoriaLink

class Categoria(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    nome:str
    descricao:Optional[str] = None

    posts: List["Post"] = Relationship(back_populates="categorias", link_model=PostCategoriaLink)