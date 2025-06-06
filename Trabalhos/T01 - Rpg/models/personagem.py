from pydantic import BaseModel, Field

class Personagem(BaseModel):
    id: int
    nome: str
    classe: str
    nivel: int = Field(ge=1)
    pontos_vida: int = Field(ge=0)
