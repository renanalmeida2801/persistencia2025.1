from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PostCreate(BaseModel):
    titulo:str
    conteudo:str
    autor_id:int
    categoria_ids: Optional[List[int]] = []

class PostRead(BaseModel):
    id:int
    titulo:str
    conteudo:str
    data_criacao:datetime
    autor_id: int

    class config:
        orm_mode = True