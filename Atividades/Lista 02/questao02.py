import pytesseract
from PIL import Image
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path: str, output_txt: str, lang: str = 'eng') -> None:
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Imagem não encontrada {image_path}")
    
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, lang=lang)

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Texto extraído salvo em: {output_txt}")

if __name__ == "__main__":
    caminho_imagem = 'outraimagem.jpg'
    arquivo_saida = 'resultado.txt'
    extract_text_from_image(caminho_imagem, arquivo_saida, lang='eng')