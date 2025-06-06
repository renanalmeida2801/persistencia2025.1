from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome:str
    email:str
    senha:str

class UsuarioRead(BaseModel):
    id:int
    nome:str
    email:str

    class config:
        orm_mode = True