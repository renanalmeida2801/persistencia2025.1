from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Curtida(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    data: datetime = Field(default_factory=datetime.utcnow)

    usuario_id: int = Field(foreign_key="usuario.id")
    post_id: int = Field(foreign_key="post.id")

    usuario: Optional["Usuario"] = Relationship(back_populates="curtidas")
    post: Optional["Post"] = Relationship(back_populates="curtidas")