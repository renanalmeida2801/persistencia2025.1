import requests
from bs4 import BeautifulSoup

def extract_title_and_links(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else 'Sem titulo encontrado'
    print(f'titulo da pagina: {title}\n')


    print('Links encontrados:')
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True) or href
        print(f' - {text}: {href}')

if __name__ == "__main__":
    url = 'https://www.ufc.br/restaurante/cardapio/5-restaurante-universitario-de-quixada'
    extract_title_and_links(url)

