from pydantic import BaseModel
from typing import Optional

class CategoriaCreate(BaseModel):
    nome:str
    descricao: Optional[str] = None

class CategoriaRead(BaseModel):
    id:int
    nome:str
    descricao:Optional[str] = None

    class config:
        orm_mode = True