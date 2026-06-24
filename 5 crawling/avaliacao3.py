import time
import urllib.robotparser
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

SECONDS = 2
BASE_URL = 'https://disciplinas.politecnico.ufsm.br/~dpadp0291/'

visited = set()

rp = urllib.robotparser.RobotFileParser()
rp.set_url(BASE_URL + "/robots.txt")
rp.read()


def find_root_links():
    global link_paths
    url = BASE_URL

    while url and url not in visited:

        if not rp.can_fetch("*", url):
            print(f"Acesso bloqueado: {url}")
            break

        print(f"\nAcessando: {url}")

        visited.add(url)

        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        a_element = soup.find_all('a')
        link_paths = []
        for link in a_element:
            link_paths.append(link['href'])

    return link_paths

def noticias(path):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(BASE_URL + "/robots.txt")
    rp.read()

    url = BASE_URL + path

    while url and url not in visited:

        if not rp.can_fetch("*", url):
            print(f"Acesso bloqueado: {url}")
            break

        print(f"\nAcessando: {url}")

        visited.add(url)

        response = urlopen(url)
        html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        page_title = soup.find('h2')
        page_title = page_title.text
        article_title = soup.find_all('h4', class_='titulo-noticia')
        article_text = soup.find_all('p', class_='resumo')
        article_date = soup.find_all('span', class_='data-post')
        article_titles = [article.contents for article in article_title]
        article_texts = [article.contents for article in article_text]
        article_dates = [article.contents for article in article_date]

        news_page_full_text = [page_title, article_titles, article_texts, article_dates]
        print("Conteudo textual da pagina de noticias")
        print(news_page_full_text)
        return news_page_full_text

def admin_usuarios(path):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(BASE_URL + "/robots.txt")
    rp.read()

    url = BASE_URL + path
    print(f"\nAcessando: {url}")

    while url and url not in visited:

        if rp.can_fetch("*", path):
            print(f"Acesso bloqueado por restrições no robots.txt: {url}")
            break

def contato(path):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(BASE_URL + "/robots.txt")
    rp.read()

    url = BASE_URL + path

    while url and url not in visited:

        if not rp.can_fetch("*", url):
            print(f"Acesso bloqueado: {url}")
            break

        print(f"\nAcessando: {url}")

        visited.add(url)

        response = urlopen(url)
        html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h2', class_='mb-0').text
        lead = soup.find('p', class_='lead').text
        strongs = soup.find_all('strong')
        strongs = [strong.text for strong in strongs]

        # name = soup.find('span', id_='dept-nome').text
        deptos = soup.find_all('span')
        deptos = [depto.text for depto in deptos]
        warning = soup.find('div', class_='mt-4').text

        news_page_full_text = [title, lead, strongs, deptos, warning]
        print("Conteudo textual da pagina de contato")
        print(news_page_full_text)
        return news_page_full_text

def produtos(path):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(BASE_URL + "/robots.txt")
    rp.read()

    url = BASE_URL + path

    while url and url not in visited:

        if not rp.can_fetch("*", url):
            print(f"Acesso bloqueado: {url}")
            break

        print(f"\nAcessando: {url}")

        visited.add(url)

        response = urlopen(url)
        html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h2', class_='mb-4').text

        card_title = soup.find_all('h5', class_='card-title')
        card_text = soup.find_all('p', class_='card-text')
        preco_venda = soup.find_all('h4', class_='preco-venda')
        disponivel = soup.find_all('span', class_='badge')
        card_title = [card_title.text for card_title in card_title]
        card_text = [card_text.text for card_text in card_text]
        preco_venda = [preco_venda.text for preco_venda in preco_venda]
        disponivel = [disponivel.text for disponivel in disponivel]

        news_page_full_text = [card_title, card_text, preco_venda, disponivel]
        print("Conteudo textual da pagina de produto")
        print(news_page_full_text)

        next = soup.find_all('a', class_='page-link')

        for i in next:
            link = BASE_URL + i['href']

        if next and next:
            next = next[1]['href']
            if next != '#':
                time.sleep(SECONDS)
                produtos(next)
        else:
            url = None

try:
    link_paths = find_root_links()
    print(link_paths)

    for link_path in link_paths:
        time.sleep(SECONDS)
        match link_path:
            case 'noticias.html':

                noticias(link_path)
            case 'contato.html':
                contato(link_path)
            case 'admin_usuarios.html':
                admin_usuarios(link_path)
            case 'produtos_pag1.html':
                produtos(link_path)

    # for link in link_paths:
    #     find_texts(link)

except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
except AttributeError as e:
    print(e)
