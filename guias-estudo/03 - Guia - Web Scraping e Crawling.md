# Web Scraping & Crawling — Guia de Estudo

> 🎯 **Foco**: Extração de dados da web com Python — `urllib` + `BeautifulSoup` + Crawling iterativo/recursivo
> Baseado nas pastas: [`05 - Web Scraping/`](../05%20-%20Web%20Scraping/) e [`06 - Web Crawling/`](../06%20-%20Web%20Crawling/)

---

## Sumário

- [Quick Reference — Código Mínimo](#quick-reference--código-mínimo)
  - [Scraping: Baixar e Parsing HTML](#scraping-baixar-e-parsing-html)
  - [Crawling Iterativo](#crawling-iterativo)
  - [Crawling Recursivo](#crawling-recursivo)
  - [Salvar em CSV](#salvar-em-csv)
  - [Robots.txt + match/case](#robotstxt--matchcase)
- [Guia Detalhado](#guia-detalhado)
  - [1. Web Scraping com urllib + BeautifulSoup](#1-web-scraping-com-urllib--beautifulsoup)
  - [2. Navegação na Árvore HTML](#2-navegação-na-árvore-html)
  - [3. Regex e Lambda no BeautifulSoup](#3-regex-e-lambda-no-beautifulsoup)
  - [4. Headers e User-Agent](#4-headers-e-user-agent)
  - [5. Tratamento de Exceções](#5-tratamento-de-exceções)
  - [6. Crawling Iterativo vs Recursivo](#6-crawling-iterativo-vs-recursivo)
  - [7. Robots.txt e Polidez](#7-robotstxt-e-polidez)
  - [8. CSV Export com csv.DictWriter](#8-csv-export-com-csvdictwriter)
  - [9. Match/Case para Roteamento](#9-matchcase-para-roteamento)
  - [10. Padrão Completo — Projeto Final](#10-padrão-completo--projeto-final)
- [Exercícios Resolvidos](#exercícios-resolvidos)

---

## Quick Reference — Código Mínimo

### Scraping: Baixar e Parsing HTML

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://example.com"
resposta = urlopen(url)          # baixa o HTML
html = resposta.read()           # lê os bytes
soup = BeautifulSoup(html, 'html.parser')

# Extrair dados
soup.find('h1')                          # primeira tag <h1>
soup.find_all('p')                       # todas as tags <p>
soup.find_all('div', class_='card')      # <div class="card">
tag.get_text()                           # texto interno (sem HTML)
tag['href']                              # valor do atributo href
tag.attrs                                # dicionário com todos os atributos
```

### Crawling Iterativo

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

url = "https://quotes.toscrape.com"
visitados = set()

while url and url not in visitados:
    visitados.add(url)
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    for q in soup.find_all('div', class_='quote'):
        texto = q.find('span', class_='text').get_text()
        autor = q.find('small', class_='author').get_text()
        print(f"{texto} — {autor}")

    proxima = soup.find('li', class_='next')
    if proxima:
        link = proxima.find('a')['href']
        url = "https://quotes.toscrape.com" + link
        time.sleep(1)
    else:
        url = None
```

### Crawling Recursivo

```python
visitados = set()

def crawl(url):
    if url in visitados:
        return
    visitados.add(url)

    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    for q in soup.find_all('div', class_='quote'):
        print(q.find('span', class_='text').get_text())

    proxima = soup.find('li', class_='next')
    if proxima:
        link = proxima.find('a')['href']
        time.sleep(1)
        crawl("https://quotes.toscrape.com" + link)

crawl("https://quotes.toscrape.com")
```

### Salvar em CSV

```python
import csv

dados = [
    {'categoria': 'produto', 'nome': 'Monitor 24', 'preco': 1450.90},
    {'categoria': 'noticia', 'nome': 'Workshop Python', 'preco': 0.0},
]

campos = ['categoria', 'nome', 'preco']

with open('dataset.csv', 'w', newline='', encoding='utf-8-sig') as f:
    escritor = csv.DictWriter(f, fieldnames=campos, delimiter=';')
    escritor.writeheader()
    escritor.writerows(dados)
```

### Robots.txt + match/case

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://site.com/robots.txt")
rp.read()

if rp.can_fetch("*", url):
    # pode acessar
    pass

# Roteamento com match/case (Python 3.10+)
match link_path:
    case 'noticias.html':
        noticias(link_path)
    case 'contato.html':
        contato(link_path)
    case 'admin_usuarios.html':
        admin_usuarios(link_path)
    case _:
        print(f"Desconhecido: {link_path}")
```

---

## Guia Detalhado

### 1. Web Scraping com urllib + BeautifulSoup

#### Fazer uma requisição HTTP

```python
from urllib.request import urlopen

resposta = urlopen("https://example.com")
html = resposta.read()          # bytes
print(resposta.status)          # 200 (código HTTP)
```

`urlopen()` retorna um objeto `http.client.HTTPResponse`. O método `.read()` devolve o conteúdo como bytes. Para converter para string: `html.decode('utf-8')`, mas o BeautifulSoup aceita bytes diretamente.

#### Parsear HTML com BeautifulSoup

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
```

O segundo parâmetro é o parser: `'html.parser'` (nativo do Python), `'lxml'` (mais rápido, requer instalação) ou `'html5lib'`.

#### Buscar tags: `find()` e `find_all()`

| Método | Retorna | Descrição |
|--------|---------|-----------|
| `soup.find('tag')` | `Tag` ou `None` | Primeira ocorrência |
| `soup.find_all('tag')` | `list` de `Tag` | Todas as ocorrências |
| `soup.find_all('tag', limit=3)` | `list` | Limita o resultado |
| `soup.find_all('div', class_='card')` | `list` | Filtra por classe (nota: `class_` com underscore) |
| `soup.find_all('a', string='Clique aqui')` | `list` | Filtra por texto exato |
| `soup.find(id='main')` | `Tag` ou `None` | Busca por id |

#### Extrair texto e atributos

```python
tag = soup.find('a')

tag.get_text()           # texto interno (remove todas as tags filhas)
tag.text                 # mesmo que get_text()
tag['href']              # valor do atributo href
tag.get('href')          # mesmo que acima, mas não lança KeyError se não existir
tag.attrs                # dicionário de todos os atributos: {'href': '...', 'class': ['...']}
```

> 💡 Prefira `tag.get('attr')` em vez de `tag['attr']` para evitar `KeyError`.

#### Extrair dados de múltiplos elementos

```python
for artigo in soup.find_all('article'):
    titulo = artigo.find('h2').get_text()
    link = artigo.find('a')['href']
    data = artigo.find('span', class_='date').get_text()
    print(titulo, link, data)
```

---

### 2. Navegação na Árvore HTML

BeautifulSoup trata o HTML como uma árvore de objetos `Tag` e `NavigableString`.

#### Filhos e descendentes

```python
# .children — iterador sobre FILHOS diretos (apenas 1 nível)
for filho in soup.body.children:
    print(filho.name)

# .descendants — iterador sobre TODOS os descendentes (recursivo)
for desc in soup.body.descendants:
    if desc.name:  # ignora strings soltas
        print(desc.name)
```

#### Pais

```python
tag.parent                  # tag pai imediato (ou None)
tag.parents                 # iterador sobre TODOS os ancestrais
for pai in tag.parents:
    print(pai.name)         # sobe: body, html, [document]
```

#### Irmãos (siblings)

```python
tag.next_sibling            # próximo irmão (pode ser string com whitespace)
tag.previous_sibling        # irmão anterior
tag.next_siblings           # iterador sobre TODOS os próximos irmãos
tag.previous_siblings       # iterador sobre TODOS os irmãos anteriores
```

> ⚠️ Os siblings incluem quebras de linha e espaços como `NavigableString`. Muitas vezes é mais prático usar `find_next_sibling()` e `find_previous_sibling()`.

```python
tag.find_next_sibling('div')     # próximo irmão que seja <div>
tag.find_previous_sibling('div') # irmão anterior que seja <div>
```

---

### 3. Regex e Lambda no BeautifulSoup

#### Busca com expressão regular

```python
import re

# Tags que começam com 'h' (h1, h2, h3, ...)
soup.find_all(re.compile(r'^h[1-6]$'))

# Classes que contêm 'card'
soup.find_all(class_=re.compile(r'card'))

# Links que contêm 'produto' no href
soup.find_all('a', href=re.compile(r'produto'))
```

#### Busca com função lambda

```python
# Tags que têm exatamente 2 atributos de classe
soup.find_all(lambda tag: len(tag.get('class', [])) == 2)

# Tags <a> que NÃO têm href
soup.find_all(lambda tag: tag.name == 'a' and not tag.get('href'))

# Tags com texto específico
soup.find_all(lambda tag: tag.name == 'p' and 'Python' in tag.get_text())
```

---

### 4. Headers e User-Agent

Alguns sites bloqueiam bots que não se identificam. Use um User-Agent de navegador real:

```python
from urllib.request import Request, urlopen

url = "https://site-que-exige-user-agent.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

req = Request(url, headers=headers)
resposta = urlopen(req)
```

Headers comuns:

| Header | Valor típico |
|--------|-------------|
| `User-Agent` | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...` |
| `Accept` | `text/html,application/xhtml+xml,...` |
| `Accept-Language` | `pt-BR,pt;q=0.9,en;q=0.8` |

> 🔁 Também é possível criar um `Opener` com `build_opener()` para reutilizar headers em múltiplas requisições.

---

### 5. Tratamento de Exceções

Sempre envolva chamadas de rede em try/except:

```python
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

url = "https://exemplo.com"

try:
    resposta = urlopen(url)
    html = resposta.read()
    soup = BeautifulSoup(html, 'html.parser')
    titulo = soup.find('h1').get_text()

except HTTPError as e:
    print(f"Erro HTTP {e.code}: {e.reason}")
    # 403 → Forbidden (talvez precise de User-Agent)
    # 404 → Not Found
    # 500 → Erro interno do servidor

except URLError as e:
    print(f"Erro de conexão: {e.reason}")
    # DNS não resolveu, servidor fora do ar, etc.

except AttributeError as e:
    print(f"Tag não encontrada: {e}")
    # soup.find('x') retornou None e você tentou .get_text()
```

**Hierarquia de exceções:**
- `HTTPError` (subclasse de `URLError`) — código HTTP 4xx/5xx
- `URLError` — problemas de rede/DNS
- `AttributeError` — tentar acessar método/atributo em `None` (tag não encontrada)

---

### 6. Crawling Iterativo vs Recursivo

#### Iterativo (while loop)

Usa um loop `while` com uma variável `url` que é atualizada a cada iteração:

```python
url = "https://quotes.toscrape.com"
visitados = set()

while url and url not in visitados:
    visitados.add(url)
    soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
    # ... extrair dados ...
    # atualizar url para a próxima página (ou None se acabou)
```

**Prós**: Fácil de entender, stack não cresce, controle explícito.
**Contras**: Precisa gerenciar manualmente a fila de URLs.

#### Recursivo (função chama a si mesma)

A função `crawl()` chama a si mesma para a próxima página:

```python
visitados = set()

def crawl(url):
    if url in visitados:
        return
    visitados.add(url)
    # ... extrair dados ...
    if proxima:
        time.sleep(1)
        crawl(proxima_url)  # ← recursão
```

**Prós**: Código mais limpo, a própria pilha de chamadas funciona como fila.
**Contras**: Risco de `RecursionError` se o site for muito profundo (>1000 páginas). Para a maioria dos casos práticos, funciona bem.

> ⚠️ Sempre tenha um **critério de parada** (`if url in visitados: return`) para evitar loops infinitos.

#### Conjunto de visitados

```python
visitados = set()   # ou visited = set()

# Antes de processar a URL:
if url in visitados:
    # já foi processada — pular
    continue   # (no while) ou return (na recursão)

visitados.add(url)
```

---

### 7. Robots.txt e Polidez

#### robots.txt

O arquivo `robots.txt` informa quais partes do site podem ou não ser acessadas por bots.

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://site.com/robots.txt")
rp.read()

if rp.can_fetch("*", url):     # "*" = qualquer user-agent
    print(f"✅ Pode acessar: {url}")
else:
    print(f"❌ Bloqueado: {url}")
```

Uso completo no crawler:

```python
BASE_URL = "https://site.com"
rp = urllib.robotparser.RobotFileParser()
rp.set_url(BASE_URL + "/robots.txt")
rp.read()

def crawl(url):
    if not rp.can_fetch("*", url):
        print(f"Acesso bloqueado pelo robots.txt: {url}")
        return
    # ... processar ...
```

#### Polidez — time.sleep()

Sites podem bloquear crawlers que fazem muitas requisições em curto espaço de tempo. Sempre aguarde entre requisições:

```python
import time

SECONDS = 2   # ou 1, ou 3 — quanto maior, mais educado

# depois de processar uma página:
time.sleep(SECONDS)
```

---

### 8. CSV Export com csv.DictWriter

```python
import csv

dados = [
    {'categoria': 'produto', 'nome': 'Monitor 24', 'preco': 1450.90, 'info': 'Tela 4K'},
    {'categoria': 'noticia', 'nome': 'Workshop Python', 'preco': 0.0, 'info': 'Prédio 70'},
]

campos = ['categoria', 'nome', 'preco', 'info']

try:
    with open('dataset.csv', 'w', newline='', encoding='utf-8-sig') as f:
        escritor = csv.DictWriter(f, fieldnames=campos, delimiter=';')
        escritor.writeheader()
        escritor.writerows(dados)
    print(f"CSV gerado com {len(dados)} linhas.")
except Exception as e:
    print(f"Erro ao salvar CSV: {e}")
```

| Detalhe | Por quê |
|---------|---------|
| `newline=''` | Evita linhas em branco extras no Windows |
| `encoding='utf-8-sig'` | Garante que acentos apareçam corretamente no Excel |
| `delimiter=';'` | Padrão brasileiro (Excel separa por `;`) |
| `fieldnames` | Define a ordem das colunas |

---

### 9. Match/Case para Roteamento

Python 3.10 introduziu `match/case` (structural pattern matching). Útil para rotear URLs para funções específicas:

```python
match link_path:
    case 'noticias.html':
        noticias(link_path)
    case 'contato.html':
        contato(link_path)
    case 'admin_usuarios.html':
        admin_usuarios(link_path)
    case 'produtos_pag1.html':
        produtos(link_path)
    case _:
        print(f"Link desconhecido: {link_path}")
```

Funciona como um `switch` de outras linguagens, mas com pattern matching mais poderoso. Cada `case` é testado em ordem; o `case _` é o *default* (coringa).

Exemplo com extração de dados dentro de cada rota:

```python
def noticias(path):
    url = BASE_URL + path
    soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
    titulos = soup.find_all('h4', class_='titulo-noticia')
    textos = soup.find_all('p', class_='resumo')
    datas = soup.find_all('span', class_='data-post')
    return [t.get_text() for t in titulos]
```

---

### 10. Padrão Completo — Projeto Final

Estrutura recomendada para um crawler completo:

```python
import time
import csv
import urllib.robotparser
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup

BASE_URL = 'https://disciplinas.politecnico.ufsm.br/~dpadp0291/'
SECONDS = 2
visited = set()

# 1. Configurar robots.txt
rp = urllib.robotparser.RobotFileParser()
rp.set_url(BASE_URL + "/robots.txt")
rp.read()

# 2. Crawler principal
def find_root_links():
    url = BASE_URL
    while url and url not in visited:
        if not rp.can_fetch("*", url):
            break
        visited.add(url)
        soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
        return [link['href'] for link in soup.find_all('a')]

# 3. Funções específicas para cada rota
def noticias(path): ...
def contato(path): ...
def admin_usuarios(path): ...
def produtos(path): ...

# 4. Main — crawling + roteamento
try:
    link_paths = find_root_links()
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

except HTTPError as e:
    print(f"HTTP Error: {e}")
except URLError as e:
    print(f"URL Error: {e}")
except AttributeError as e:
    print(f"Attribute Error: {e}")
```

---

## Exercícios Resolvidos

| Exercício | Resolução |
|-----------|-----------|
| 🕷️ Web Crawling — Quotes | [📄 Resolução comentada](resolucoes/06%20-%20resolucao%20-%20web%20crawling.md) |
| 📦 Trabalho 1 — Scraping e Crawling | [📄 Resolução comentada](resolucoes/07%20-%20resolucao%20-%20trabalho%201%20scraping%20crawling.md) |

---

> 📎 **Arquivos originais da disciplina**:
> - [`05 - Web Scraping/01 - Slides - Web Scraping.odp`](../05%20-%20Web%20Scraping/01%20-%20Slides%20-%20Web%20Scraping.odp)
> - [`05 - Web Scraping/02 - Slides - Web Scraping Parte 2.odp`](../05%20-%20Web%20Scraping/02%20-%20Slides%20-%20Web%20Scraping%20Parte%202.odp)
> - [`06 - Web Crawling/01 - Slides - Web Crawling.odp`](../06%20-%20Web%20Crawling/01%20-%20Slides%20-%20Web%20Crawling.odp)
> - [`06 - Web Crawling/02 - Exemplo - Crawling Basico.py`](../06%20-%20Web%20Crawling/02%20-%20Exemplo%20-%20Crawling%20Basico.py)
> - [`06 - Web Crawling/03 - Exemplo - Crawling Recursivo.py`](../06%20-%20Web%20Crawling/03%20-%20Exemplo%20-%20Crawling%20Recursivo.py)
> - [`06 - Web Crawling/04 - Exemplo - Criacao CSV.py`](../06%20-%20Web%20Crawling/04%20-%20Exemplo%20-%20Criacao%20CSV.py)
> - [`06 - Web Crawling/07 - Avaliacao - Web Crawling.py`](../06%20-%20Web%20Crawling/07%20-%20Avaliacao%20-%20Web%20Crawling.py)
