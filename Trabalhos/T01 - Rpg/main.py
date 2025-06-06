
from fastapi import FastAPI
from controllers import personagem_controller, habilidade_controller, equipamento_controller

app = FastAPI()

app.include_router(personagem_controller.router)
app.include_router(habilidade_controller.router)
app.include_router(equipamento_controller.router)
