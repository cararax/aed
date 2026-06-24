# Resolução — Exercício de Web Crawling (Loja Virtual)

## Objetivo

Construir um crawler que percorre as páginas de produtos de uma loja virtual, extraindo nome e preço de cada produto e avançando pela paginação até o fim.

---

## Código completo

```python
"""
Crawler para https://webscraper.io/test-sites/e-commerce/static

Percorre todas as páginas de produtos, extrai nome e preço de cada item
e exibe um resumo ao final.

Funcionalidades bônus:
  - Contagem total de produtos
  - Armazenamento em lista de dicionários
  - Filtro por preço (exibe apenas produtos acima de um valor)
  - Limite opcional de páginas percorridas (ex.: 2 páginas)
"""

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import time

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------------------------
URL_INICIAL = "https://webscraper.io/test-sites/e-commerce/static"
LIMITE_PAGINAS = 2       # None = sem limite; 2 = apenas 2 páginas
FILTRO_PRECO_MIN = 0     # Exibe apenas produtos com preço >= este valor
PAUSA_SEGUNDOS = 1       # Pausa entre requisições (polite crawling)

# ---------------------------------------------------------------------------
# ESTRUTURA DE DADOS
# ---------------------------------------------------------------------------
# Lista que acumulará todos os produtos encontrados em TODAS as páginas.
# Cada produto é um dicionário com as chaves 'nome' e 'preco'.
todos_produtos = []

# Conjunto que armazena URLs já visitadas para evitar loops.
visitadas = set()

# Contador de páginas processadas (usado com LIMITE_PAGINAS).
pagina_atual = 0

# ---------------------------------------------------------------------------
# LOOP PRINCIPAL (while)
# ---------------------------------------------------------------------------
# O loop começa com a URL inicial e avança para a próxima página enquanto
# houver um link de paginação válido. A variável 'url' é atualizada a cada
# iteração: ou recebe o href da página seguinte, ou recebe None (fim).

url = URL_INICIAL

while url and url not in visitadas:

    # --- Controle de limite de páginas ---
    # Se um limite foi definido, interrompe ao atingi-lo.
    if LIMITE_PAGINAS is not None and pagina_atual >= LIMITE_PAGINAS:
        print(f"\n[LIMITE] Páginas limitadas a {LIMITE_PAGINAS}. Parando.\n")
        break

    # --- Marca a URL atual como visitada ---
    # Isso evita que o crawler entre em loop infinito caso haja um ciclo
    # na paginação (ex.: "próxima" apontar para a primeira página).
    visitadas.add(url)
    pagina_atual += 1

    print(f"\n--- Página {pagina_atual}: {url} ---")

    # --- Requisição HTTP ---
    # Usamos urlopen() do módulo urllib.request. Ela retorna um objeto
    # response que contém o HTML da página. O bloco try/except captura
    # erros de rede (URLError) e erros HTTP (HTTPError, ex.: 404).
    try:
        resposta = urlopen(url)
        html = resposta.read()
    except HTTPError as e:
        print(f"  [ERRO HTTP] Código {e.code} ao acessar {url}")
        break
    except URLError as e:
        print(f"  [ERRO REDE] {e.reason} ao acessar {url}")
        break

    # --- Parse do HTML com BeautifulSoup ---
    # 'html.parser' é o parser embutido do Python (não requer instalação
    # adicional). Ele transforma o HTML bruto em uma árvore de objetos
    # que podemos navegar com métodos como find_all(), find(), select().
    soup = BeautifulSoup(html, 'html.parser')

    # ------------------------------------------------------------------
    # EXTRAÇÃO DE DADOS: produtos (.thumbnail)
    # ------------------------------------------------------------------
    # Cada produto está dentro de um <div class="thumbnail">. Essa classe
    # agrupa: imagem, link do título (<a class="title">), preço
    # (<h4 class="price">) e descrição.
    #
    # Estrutura esperada:
    #   <div class="thumbnail">
    #     <a class="title" href="...">Nome do Produto</a>
    #     <h4 class="price">$19.99</h4>
    #     ...
    #   </div>
    #
    # Usamos soup.find_all() com o seletor CSS 'div.thumbnail' para
    # obter todos os cartões de produto da página atual.
    thumbnails = soup.find_all('div', class_='thumbnail')

    if not thumbnails:
        print("  [AVISO] Nenhum produto encontrado nesta página.")

    # Para cada cartão de produto, extraímos nome e preço.
    # .get_text(strip=True) retorna o texto interno do elemento sem
    # espaços extras nas bordas.
    for cartao in thumbnails:
        # --- Nome do produto ---
        # Localizamos o <a> com class="title" DENTRO do cartão atual.
        # O método find() busca apenas entre os descendentes do cartão.
        elemento_nome = cartao.find('a', class_='title')

        # --- Preço do produto ---
        # Localizamos o <h4> com class="price".
        elemento_preco = cartao.find('h4', class_='price')

        # --- Tratamento de elementos ausentes ---
        # Se por algum motivo o HTML estiver mal formatado e o elemento
        # não existir, usamos um fallback ('<sem nome>', '<sem preço>').
        # Isso evita que o crawler quebre com AttributeError.
        nome = elemento_nome.get_text(strip=True) if elemento_nome else '<sem nome>'
        preco = elemento_preco.get_text(strip=True) if elemento_preco else '<sem preço>'

        produto = {'nome': nome, 'preco': preco}
        todos_produtos.append(produto)

    # ------------------------------------------------------------------
    # PAGINAÇÃO: detectando o link da próxima página
    # ------------------------------------------------------------------
    # A paginação do site está dentro de um <ul class="pagination">.
    # Dentro dela, há vários <li> com <a>. O <li> da página atual tem
    # class="page-item active" (sem link clicável). O <li> da página
    # seguinte (se existir) tem class="page-item" com um <a>.
    #
    # Estratégia: encontramos o <a> cujo texto seja "›" (seta para
    # direita) — este é o link "Next". Se ele existir e não tiver a
    # classe "disabled", significa que há uma próxima página.
    #
    # Caso a seta "›" não seja encontrada (ex.: sites com numeração),
    # podemos buscar o <a> com rel="next" (padrão HTML5), ou então
    # localizar o <li> que contém um link cujo href seja diferente de
    # '#' e diferente do atual.

    pagination = soup.find('ul', class_='pagination')
    proximo_link = None

    if pagination:
        # --- Abordagem 1: link "›" (Next) ---
        # Percorre todos os <a> dentro da paginação e verifica se o
        # texto é "›". Se encontrar, usa seu href.
        for link in pagination.find_all('a'):
            if link.get_text(strip=True) == '›':
                href = link.get('href')
                # Alguns sites usam '#' como placeholder para disabled.
                if href and href != '#':
                    # Concatena o href relativo com a base.
                    # Ex.: href = "/test-sites/e-commerce/static/computers/laptops?page=2"
                    # URL completa = "https://webscraper.io" + href
                    proximo_link = "https://webscraper.io" + href
                break

        # --- Abordagem alternativa (caso "›" não exista) ---
        # Se a abordagem 1 não encontrou, podemos tentar localizar
        # o último <a> que não seja '#' e nem o href atual.
        if not proximo_link:
            pag_links = pagination.find_all('a')
            for link in pag_links:
                href = link.get('href', '')
                if href and href != '#' and href not in url:
                    # Pega o penúltimo ou último link válido
                    proximo_link_candidato = href

            if proximo_link_candidato:
                # Se o href for relativo, concatena com a base.
                if proximo_link_candidato.startswith('http'):
                    proximo_link = proximo_link_candidato
                else:
                    proximo_link = "https://webscraper.io" + proximo_link_candidato

    # --- Atualiza a url para a próxima iteração ---
    # Se encontramos um próximo link, avançamos. Caso contrário,
    # atribuímos None para encerrar o loop while.
    url = proximo_link

    # --- Pausa de cortesia (polite crawling) ---
    # Aguarda um intervalo entre requisições para não sobrecarregar
    # o servidor. Essencial em crawlers reais.
    if url:
        time.sleep(PAUSA_SEGUNDOS)

# ---------------------------------------------------------------------------
# RESUMO FINAL
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("  CRAWLING FINALIZADO")
print("=" * 60)
print(f"  Páginas visitadas: {pagina_atual}")
print(f"  Total de produtos encontrados: {len(todos_produtos)}")

# --- Listagem de todos os produtos ---
print("\n  Produtos encontrados:")
for i, p in enumerate(todos_produtos, 1):
    print(f"  {i:3d}. {p['nome']:50s} {p['preco']}")

# ---------------------------------------------------------------------------
# BÔNUS 1: Lista de dicionários (já implementada acima)
# ---------------------------------------------------------------------------
# A variável `todos_produtos` é uma lista de dicionários. Cada dicionário
# tem as chaves 'nome' e 'preco'. Isso facilita exportar para CSV, JSON,
# ou aplicar filtros.

# ---------------------------------------------------------------------------
# BÔNUS 2: Filtro por preço
# ---------------------------------------------------------------------------
# Exibe apenas produtos cujo preço (convertido para float) seja maior ou
# igual a FILTRO_PRECO_MIN. A conversão remove o caractere '$' e espaços.
print(f"\n  Produtos com preço >= ${FILTRO_PRECO_MIN:.2f}:")
for i, p in enumerate(todos_produtos, 1):
    try:
        # Remove o '$' do início e converte para float.
        preco_num = float(p['preco'].replace('$', '').strip())
        if preco_num >= FILTRO_PRECO_MIN:
            print(f"  {i:3d}. {p['nome']:50s} {p['preco']}")
    except (ValueError, AttributeError):
        # Se o preço não for conversível (ex.: '<sem preço>'), exibimos
        # mesmo assim.
        print(f"  {i:3d}. {p['nome']:50s} {p['preco']} (preço não numérico)")

# ---------------------------------------------------------------------------
# BÔNUS 3: Limite de páginas (já implementado no início do while)
# ---------------------------------------------------------------------------
# A variável LIMITE_PAGINAS controla quantas páginas o crawler percorre.
# Quando definida como 2, o loop é interrompido após processar 2 páginas.
```
