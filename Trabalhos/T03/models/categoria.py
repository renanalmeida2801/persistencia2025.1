from pydantic import BaseModel, Field
from uuid import uuid4

class Categoria(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Identificador único da categoria")
    nome: str = Field(..., description="Nome da categoria")
    descricao: str = Field(..., description="Descrição da categoria")
    publico_alvo: str = Field(..., description="Público-alvo típico da categoria")
    popularidade: int = Field(...,ge=1, le=5, description="Nível de popularidade de 1 a 5")