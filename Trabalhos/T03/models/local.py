from pydantic import BaseModel, Field
from uuid import uuid4

class Local(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Identificador único do local")
    nome: str = Field(..., description="Nome do local")
    endereco: str = Field(..., description="Endereço completo do local")
    cidade: str = Field(..., description="Cidade onde o local esta localizado")
    estado: str = Field(..., description="Estado onde o local esta localizado")
    capacidade: int = Field(...,ge=0, description="Capacidade máxima de pessoas")