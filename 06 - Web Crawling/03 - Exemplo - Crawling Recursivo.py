from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

visitados = set()

def crawl(url):
    if url in visitados:
        return
    visitados.add(url)

    print(f"Acessando: {url}")
    resposta = urlopen(url)
    html = resposta.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Imprime as citações da página
    for q in soup.find_all('div', class_='quote'):
        texto = q.find('span', class_='text').get_text()
        autor = q.find('small', class_='author').get_text()
        print(f"{texto} — {autor}")

    # Busca próxima página e chama a função novamente
    proxima = soup.find('li', class_='next')
    if proxima:
        link = proxima.find('a')['href']
        proxima_url = "https://quotes.toscrape.com" + link
        time.sleep(1)
        crawl(proxima_url)

# Início
crawl("https://quotes.toscrape.com")
