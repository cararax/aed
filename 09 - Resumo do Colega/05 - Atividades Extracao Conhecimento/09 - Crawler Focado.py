# Base padrão para scraping
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import sys

sys.stdout.reconfigure(encoding='utf-8') # Se não o terminal buga com o print

def acha_produtos_nome_preco(sopa):
    lista_produtos = []
    produtos = sopa.find_all("div", {"class": "card thumbnail"}) # Acha produto
    for produto in produtos: # Tira informações do produto
        try:
            #print(produto.find("a", {"class": "title"}).get_text())
            #print(produto.find("h4", {"class": "price"}).get_text())
            nome = produto.find("a", {"class": "title"}).get_text()
            preco = produto.find("h4", {"class": "price"}).get_text()
            lista_produtos.append({"nome": nome, "preco": preco})
        except AttributeError as e:
            print(e)
        else:
            continue
    return lista_produtos
        
def acha_links(sopa):
    regex_links_ecommerce = re.compile("(/test-sites/e-commerce/).*") # Só aceitar links desse domínio
    links_ecommerce = set()
    proximos_links = sopa.find_all("a")

    for proximo_link in proximos_links: # Acho todos os links da página
        href = proximo_link.get("href")
        if href is None:
            continue
        #print(href)

        link_real = re.match(regex_links_ecommerce, proximo_link.get("href")) # Filtro os que importam
        if link_real is not None:
            #print(link_real[0])
            links_ecommerce.add(link_real[0])
    return links_ecommerce
        
def ciclo_crawling(link_inicial, max_links=None):
    base = "https://webscraper.io"
    
    fila = [link_inicial]
    visitados = set()
    resultados = []

    while fila:
        if max_links is not None and len(visitados) >= max_links: # Hard impede o scraping de todos os links
            break

        caminho = fila.pop(0) 

        if caminho in visitados: # Se já visitamos o caminho, ignoramos ele
            continue

        visitados.add(caminho)

        try:
            url = base + caminho
            html = urlopen(url)
            sopa = BeautifulSoup(html.read(), 'html.parser')

            produtos = acha_produtos_nome_preco(sopa)
            resultados.extend(produtos) 

            novos_links = acha_links(sopa) # Acho todos os links do domínio relevantes dessa página

            for link in novos_links:
                if link not in visitados and link not in fila:
                    fila.append(link)

        except (HTTPError, URLError) as e:
            print(e)

    return resultados       

link_inicial = "/test-sites/e-commerce/static"
try:
    dados = ciclo_crawling(link_inicial) # Pode colocar quantos ciclos aceita
    for produto in dados:
        nome = produto["nome"].strip()
        preco = produto["preco"].strip()
        print(nome, "-", preco)
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)


















# Crie um programa em Python que: Acesse a página inicial de produtos, 
# extraia o nome e o preço dos produtos, navegue para a próxima página, continue até não haver mais páginas
# Os produtos estão em elementos com classe "thumbnail"
# O nome está em uma tag <a class="title">
# O preço está em <h4 class="price">
# A paginação está no final da página (<ul class="pagination">)

'''
        match = re.match(regex_min_seg, duracao_texto)
        if match is not None:
            minutos, segundos = match.groups()
            #print(match)
            duracao_dicionario.append({
                "minutos": minutos,
                "segundos": segundos
            })
'''
