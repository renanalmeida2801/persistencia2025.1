import yaml
import logging
import json

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

log_config = config.get("logging", {})
log_level = getattr(logging, log_config.get("level", "INFO").upper(), logging.INFO)
log_file = log_config.get("file", "app.log")
log_format = log_config.get("format", "$(asctime)s - %(levelname)s - %(message)s")

logging.basicConfig(level=log_level, filename=log_file, filemode="a", format=log_format)
logger = logging.getLogger(__name__)

logger.info("Aplicacao iniciada.")

data_file = config.get("data", {}).get("file", "data.json")

try:
    with open(data_file, "r") as f:
        data = json.load(f)
        logger.info(f"{len(data)} registros carregados do arquivo {data_file}.")
except Exception as e:
    logger.error(f"Erro ao ler arquivo JSON: {e}")
    data = []

for entry in data:
    try:
        if entry["age"] is None:
            logger.warning(f"Id {entry['id']} ({entry['name']}) tem idade ausente.")
        else:
            logger.info(f"processando Id {entry['id']}: {entry['name']} tem {entry['age']} anos.")
    except Exception as e:
        logger.error(f"erro ao processar entrada {entry}: {e}")

logger.info("Aplicacao finalizada.")