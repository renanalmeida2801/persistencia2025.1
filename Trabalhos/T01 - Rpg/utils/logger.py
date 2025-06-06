import logging
from functools import wraps

logging.basicConfig(filename="logs_api.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def registrar_log(mensagem):
    logging.info(mensagem)

def log_endpoint(nome_funcao):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            registrar_log(f"[CHAMADA] {nome_funcao} | args={args} | kwargs={kwargs}")
            resultado = func(*args, **kwargs)
            registrar_log(f"[RESPOSTA] {nome_funcao} | retorno={resultado}")
            return resultado
        return wrapper
    return decorator
