# Regex:
# /img/gifts/img[0-9]+\.jpg
#                  ou [.]

# exercicio lambda
precos=[10.0, 25.5, 7.99, 50.0, 15.75]

filtrado = list(filter(lambda precos: precos>20, precos))

for preco in filtrado:
    print (filtrado)


# exercicio 1
# Base padrão para scraping
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import sys

sys.stdout.reconfigure(encoding='utf-8') # Se não o terminal buga com o print

try:
    html = urlopen('https://disciplinas.politecnico.ufsm.br/~dpadp0291/videos.html')
    sopa = BeautifulSoup(html.read(), 'html.parser')
    print(sopa.h1.get_text())
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
else:
    print('Tudo certo. Seguir com o scraping')

acha_titulo = re.compile(r"video-titulo(-[a-z]+)?")
titulos = sopa.find_all("p", {"class":acha_titulo})

titulos_lista = []
for titulo in titulos:
    titulos_lista.append(titulo.get_text())
    #print (titulos_lista[0])

acha_duracoes = re.compile(r"Duração: ")
duracoes = sopa.find_all("p", {"class": "video-duracao"}, string=acha_duracoes)

duracao_dicionario = [] # dicionario como lista
regex_min_seg = re.compile(r"Duração: ([0-9]+m) ([0-9]{1,2}s)")
for duracao in duracoes:
    print (duracao.get_text())
    duracao_texto = duracao.get_text()
    try:
        match = re.match(regex_min_seg, duracao_texto)
        if match is not None:
            minutos, segundos = match.groups()
            #print(match)
            duracao_dicionario.append({
                "minutos": minutos,
                "segundos": segundos
            })
    except re.error as e:
        print(e)

for dicionario in duracao_dicionario:
    print(dicionario["minutos"], dicionario["segundos"])



'''
Leia o conteúdo da página videos.html e use o BeautifulSoup para localizar:
Todos os elementos <p> cuja classe contenha a palavra “titulo” (use regex para filtrar pela class);
Todos os elementos <p> cujo conteúdo comece com “Duração:” (use regex sobre o texto).

Extraia:
Os títulos dos vídeos;
As durações separadas em minutos e segundos (usando regex dentro do texto).

Exiba os resultados em formato tabular no console.
Extrair os títulos dos vídeos (começando com a palavra "Aula"), localizados em <p> com classes que contenham a palavra "titulo";
Extrair as durações dos vídeos, presentes em <p> com classes relacionadas a duração, no formato Xm Ys (minutos e segundos). Atenção: outras durações não válidas estão presentes e precisam ser ignoradas;
Pesquise como salvar os dados extraídos em um arquivo de texto.
'''
