from pydantic import BaseModel, Field
from datetime import date
from uuid import uuid4

class Artista(BaseModel):
    id: str = Field(default_factory=lambda :str(uuid4()), description="Identificador único do artista")
    nome: str = Field(..., description="Nome do artista ou do grupo")
    genero: str = Field(..., description="Gênero artistico (música, dança, poesia, etc)")
    biografia: str = Field(..., description="Mini biografia ou resumo")
    data_nascimento: date = Field(..., description="Data de nascimento")
    nacionalidade: str = Field(..., description="País de origem do artista")