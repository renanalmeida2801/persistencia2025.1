from pydantic import BaseModel
from datetime import datetime

class CurtidaCreate(BaseModel):
    usuario_id:int
    post_id:int

class CurtidaRead(BaseModel):
    id:int
    usuario_id:int
    post_id:int
    data:datetime

    class config:
        orm_mode = True