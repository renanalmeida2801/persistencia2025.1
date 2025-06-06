import os
import json
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from PIL import Image, ImageOps
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# função para extrair de um HTML
def extract_html(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.title.string if soup.title else ''
    links = [
        {"text": a.get_text(strip=True) or a["href"], "href": a["href"]}
        for a in soup.find_all("a", href=True)
    ]
    return {"title": title, "links": links}

# Função para extrair de um pdf
def extract_pdf(path):
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return {"text": "\n".join(text)}

# função para extrair texto de imagem
def extract_image(path, lang="eng"):
    img = Image.open(path)
    gray = ImageOps.grayscale(img)
    bw = gray.point(lambda x:0 if x < 128 else 255, "1")
    text = pytesseract.image_to_string(bw, lang=lang)
    return {"text": text}

# Identificaçao do tipo e roteamento
def process_resource(res):
    if res.lower().startswith("http://") or res.lower().startswith("https://"):
        data = extract_html(res)
        tipo = "html"
    else:
        ext = os.path.splitext(res)[1].lower()
        if ext == ".pdf":
            data = extract_pdf(res)
            tipo = "pdf"
        elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
            data = extract_image(res)
            tipo = "imagem"
        else:
            tipo = "desconhecido"
            data = None
    return {"resource": res, "type": tipo, "data": data}

if __name__ == "__main__":
    # Exemplo de recursos: troque pelos seus próprios!
    resources = [
        "https://si3.ufc.br/sigaa/verTelaLogin.do;jsessionid=359545C1484FC65D4289139BFC566DBC.node23",
        "Lista2Exemplo.pdf",
        "outraimagem.jpg"
    ]
    results = [process_resource(r) for r in resources]
    # Exibe em JSON organizado
    print(json.dumps(results, ensure_ascii=False, indent=2))