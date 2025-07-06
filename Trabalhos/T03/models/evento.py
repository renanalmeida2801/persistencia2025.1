from pydantic import BaseModel, Field
from datetime import date
from typing import List
from uuid import uuid4

class Evento(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Identificador unico do evento")
    nome: str = Field(..., description="Nome do evento")
    descricao: str = Field(..., description="Descrição do evento")
    data: date = Field(..., description="Data do evento")
    local_id: str = Field(..., description="Id do local onde o evento ocorre")
    categoria_id: str = Field(..., description= "ID da categoria do evento")
    artistas_ids: List[str] = Field(..., default_factory=list, description="Lista de IDs dos artistas participantes")