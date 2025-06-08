# app/database.py
from sqlmodel import create_engine, SQLModel, Session
from app.config import settings

engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    from app.models.relato import Relato
    from app.models.categoria import CategoriaFenomeno
    from app.models.entidade import EntidadeSobrenatural
    from app.models.registro import RegistroMultimidia
    from app.models.testemunha import Testemunha

    SQLModel.metadata.create_all(engine)
