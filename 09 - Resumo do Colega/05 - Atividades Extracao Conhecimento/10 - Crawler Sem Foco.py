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
    produtos = sopa.find_all("div", {"class": "card thumbnail"})
    for produto in produtos: # Acho informações produto primeira página
        #print(produto.find("a", {"class": "title"}).get_text())
        #print(produto.find("h4", {"class": "price"}).get_text())
        nome = produto.find("a", {"class": "title"}).get_text()
        preco = produto.find("h4", {"class": "price"}).get_text()
        lista_produtos.append({"nome": nome, "preco": preco})
        
def acha_links(sopa):
    regex_acha_links = re.compile("(/.*)|(https:.*)") # acha todos os links, mas não queremos todos, queremos os do test-sites
    links = set()
    proximos_links = sopa.find_all("a")

    for proximo_link in proximos_links: # Acho todos os links da página
        href = proximo_link.get("href")
        if href is None:
            continue
        #print(href)

        link_real = re.match(regex_acha_links, proximo_link.get("href"))
        if link_real is not None:
            print(link_real[0])
            links.add(link_real)
    return links
        
def ciclo_crawling(sopa):
    try:
        #print(sopa.h1.get_text())
        produtos_dict = acha_produtos_nome_preco(sopa)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    else:
        print('Tudo certo joia de cabo a rabo')
        
        
# https://webscraper.io/test-sites/e-commerce/static
# Se pegam os primeiros links
link_inicial = "https://webscraper.io/test-sites/e-commerce/static" # A página Home
html = urlopen(link_inicial)
sopa = BeautifulSoup(html.read(), 'html.parser')
links = acha_links(sopa)
# Depois que temos todos os links da primeira página damos crawling em todos eles (ou quantidade específica)


ciclo_crawling(sopa)

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
