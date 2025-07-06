from pydantic import BaseModel, Field
from uuid import uuid4

class EventoArtista(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="ID único do vínculo")
    evento_id: str = Field(..., description="ID do evento")
    artista_id: str = Field(..., description="ID do artista")
