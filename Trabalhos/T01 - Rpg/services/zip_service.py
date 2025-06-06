import zipfile

def compactar_csv_para_zip(path: str, nome_zip: str) -> str:
    with zipfile.ZipFile(nome_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(path)
    return nome_zip
