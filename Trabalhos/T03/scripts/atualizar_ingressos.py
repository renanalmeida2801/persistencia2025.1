import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db


async def atualizar_ingressos_com_evento_id():
    ingressos = await db.ingressos.find().to_list(None)
    eventos = await db.eventos.find().to_list(None)

    eventos_por_nome_data = {
        (e["nome"], e["data"]): e["id"]
        for e in eventos
    }

    atualizados = 0
    for ingresso in ingressos:
        evento_info = ingresso.get("evento")
        if not evento_info:
            continue

        chave = (evento_info["nome"], evento_info["data"])
        evento_id = eventos_por_nome_data.get(chave)

        if evento_id:
            await db.ingressos.update_one(
                {"id": ingresso["id"]},
                {"$set": {"evento_id": evento_id}}
            )
            atualizados += 1

    print(f"Ingressos atualizados com evento_id: {atualizados}")
