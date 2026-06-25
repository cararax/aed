from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8') # Se não o terminal buga com o print

html = urlopen('https://disciplinas.politecnico.ufsm.br/~dpadp0291/Scraping/catalogo_cursos.html')
sopa = BeautifulSoup(html.read(), 'html.parser')
print(sopa.h1.get_text())

primeiro_curso = sopa.find("div", {"class": "curso-card"})

#1
for filho in primeiro_curso.children:
    if filho.name is not None:
        print(filho.name)

#2
contem_professor = primeiro_curso.find(class_="curso-professor")
print(contem_professor.find_next_sibling("span").get_text())

#3
contem_valor = primeiro_curso.find(class_="valor")
print(contem_valor.parent.get_text())

'''
1 Filhos: Itere sobre os .children do elemento e imprima o nome (.name) de cada tag filha.
2 Irmão: Encontre o <span> com a classe curso-professor. A partir dele, use .find_next_sibling('span') para encontrar e imprimir o texto da tag de duração.
3 Pai: Encontre o <span> com a classe valor. Use .parent para imprimir o texto completo do seu elemento pai.


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