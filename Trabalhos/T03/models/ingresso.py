from pydantic import BaseModel, Field
from datetime import date
from uuid import uuid4

class EventoResumo(BaseModel):
    nome: str
    data: date

class Ingresso(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Identificador único do ingresso")
    evento: EventoResumo 
    quantidade: int = Field(...,  ge=1, description="Quantidade total emitida")
    preco: float = Field(..., ge=0, description="Preço unitário do ingresso")
    disponiveis: int = Field(..., description="Quantidade disponível para venda")
    data_emissao: date = Field(..., description="Data de emissão do lote de ingressos")