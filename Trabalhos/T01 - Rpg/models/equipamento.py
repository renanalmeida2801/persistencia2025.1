from pydantic import BaseModel, Field

class Equipamento(BaseModel):
    id: int
    nome: str
    tipo: str
    ataque: int = Field(ge=0)
    defesa: int = Field(ge=0)