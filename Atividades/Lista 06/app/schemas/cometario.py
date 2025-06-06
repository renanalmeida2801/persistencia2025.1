from pydantic import BaseModel
from datetime import datetime

class ComentarioCreate(BaseModel):
    conteudo:str
    autor_id:int
    post_id:int

class ComentarioRead(BaseModel):
    id:int
    conteudo: str
    data_criacao: datetime
    autor_id: int
    post_id:int

    class config:
        orm_mode = True