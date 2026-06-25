from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8') # Se não o terminal buga com o print

# Localizar cursos e for para print dos dados dos cursos. tags com find no for:
# Título: A tag h2 com a classe curso-titulo.
# Professor: A tag span com a classe curso-professor.
# Preço: A tag span com a classe valor.
html = urlopen('https://disciplinas.politecnico.ufsm.br/~dpadp0291/Scraping/catalogo_cursos.html')
sopa = BeautifulSoup(html.read(), 'html.parser')

print(sopa.h1) 

cursos = sopa.find_all("div", {"class": "curso-card"})

for curso in cursos:
    print(curso.find("h2", {"class": "curso-titulo"}))
    contem_professor = curso.find("div", {"class": "curso-meta"})
    print(contem_professor.find("span", {"class": "curso-professor"}))
    contem_valor = curso.find("div", {"class": "curso-preco"})
    print(contem_valor.find("span", {"class": "valor"}))
    #print(curso.find("h2", {"class": "curso-titulo"}))



'''
<div class="curso-card" data-lancamento="2025-01-15">
            <h2 class="curso-titulo">Introdução ao Python para Dados</h2>
            <p class="curso-descricao">
                Aprenda os fundamentos de Python e como utilizá-lo para manipulação e análise de dados com bibliotecas como Pandas e NumPy.
            </p>
            <div class="curso-meta">
                <span class="curso-professor">👨‍🏫 Prof. Dr. João Silva</span>
                <span class="curso-duracao">🕒 40 horas</span>
                <span class="curso-nivel">📈 Nível: Iniciante</span>
            </div>
            <div class="curso-preco">
                <span class="moeda">R$</span>
                <span class="valor">450,00</span>
            </div>
        </div>
'''
