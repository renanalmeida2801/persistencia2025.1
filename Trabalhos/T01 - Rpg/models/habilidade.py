from pydantic import BaseModel, Field

class Habilidade(BaseModel):
    id: int
    nome: str
    descricao: str
    custo_mana: int = Field(ge=0)
    nivel_requerido:int = Field(ge=1)