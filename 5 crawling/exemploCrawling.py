from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

url = "https://quotes.toscrape.com"
visitados = set()

while url and url not in visitados:
    print(f"Acessando: {url}")
    visitados.add(url)

    resposta = urlopen(url)
    html = resposta.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Imprime citações da página
    for q in soup.find_all('div', class_='quote'):
        texto = q.find('span', class_='text').get_text()
        autor = q.find('small', class_='author').get_text()
        print(f"{texto} — {autor}")

    # Verifica se há próxima página
    proxima = soup.find('li', class_='next')
    if proxima:
        link = proxima.find('a')['href']
        url = "https://quotes.toscrape.com" + link
        time.sleep(1)
    else:
        url = None
