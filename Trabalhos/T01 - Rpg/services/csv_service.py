import csv
import os
from typing import List
from pydantic import BaseModel

def carregar_csv(path: str, model: BaseModel) -> List[BaseModel]:
    if not os.path.exists(path):
        return []
    with open(path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [model(**{k: int(v) if v.isdigit() else v for k, v in row.items()}) for row in reader]

def salvar_csv(path: str, data: List[BaseModel], fields: List[str]):
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for d in data:
            writer.writerow(d.dict())
