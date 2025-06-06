import os
import csv
import xml.etree.ElementTree as ET
from fastapi import HTTPException

def csv_para_xml(csv_path, tag_raiz, tag_item):
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        raiz = ET.Element(tag_raiz)
        for linha in reader:
            item = ET.SubElement(raiz, tag_item)
            for chave, valor in linha.items():
                ET.SubElement(item, chave).text = valor
        tree = ET.ElementTree(raiz)
        xml_path = csv_path.replace(".csv", ".xml")
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        return xml_path
