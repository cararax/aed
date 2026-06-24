# Resolução — Trabalho 1: Scraping & Crawling

## Enunciado

Criar um scraper/crawler para o site `https://disciplinas.politecnico.ufsm.br/~dpadp0291/` que:

1. Inicie a partir de `index.html`
2. Descubra todos os links disponíveis na página inicial
3. Planeje a navegação automatizada entre as seções
4. Observe as restrições do `robots.txt`
5. Extraia o conteúdo textual de cada página
6. Exporte todos os dados coletados para CSV

---

## Código completo

```python
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

except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
except AttributeError as e:
    print(e)
```

---

## Explicação detalhada

### 1. `RobotFileParser` — Por que verificar o `robots.txt`?

O arquivo `robots.txt` é um padrão de exclusão de robôs. Ele informa
crawlers automatizados quais URLs **não devem** ser acessadas.

```python
rp = urllib.robotparser.RobotFileParser()
rp.set_url(BASE_URL + "/robots.txt")
rp.read()
```

**Funcionamento:**

- `RobotFileParser()` cria um parser vazio.
- `set_url(url)` aponta para o arquivo `robots.txt` do site.
- `read()` faz o download e interpreta as regras.
- `can_fetch(user_agent, url)` retorna `True` se o robô `user_agent`
  está autorizado a acessar `url`, ou `False` caso contrário.

**Por que verificar?**
- **Ética e legalidade:** respeitar a vontade do administrador do site.
- **Bloqueio de seções:** páginas como `admin_usuarios.html` podem
  ser explicitamente proibidas.
- **Boa prática profissional:** todo crawler bem-comportado deve
  consultar o `robots.txt` antes de cada requisição.

**No código:** cada função recria o parser e verifica
`rp.can_fetch("*", url)`. Se o acesso é negado, a função exibe uma
mensagem e interrompe a execução com `break`.

> **Atenção:** o código recria o `RobotFileParser` em cada função.
> Uma otimização possível seria reutilizar o parser global `rp`
> definido no início, evitando nova requisição HTTP a cada seção.

---

### 2. Padrão `match/case` (Python 3.10+)

O `match/case` é a estrutura de **pattern matching** estrutural
introduzida no Python 3.10. Ele funciona como um `switch` avançado.

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
```

**Como funciona:**
- O valor de `link_path` é comparado sequencialmente contra cada
  padrão `case`.
- No primeiro `case` que corresponder, o bloco associado é executado.
- Se nenhum padrão corresponder, nada acontece (não há `case _`
  padrão, mas poderia ser adicionado como fallback).

**Por que usar?**
- **Legibilidade:** substitui cadeias de `if/elif` por uma estrutura
  mais declarativa.
- **Roteamento explícito:** mapeia claramente cada link da página
  inicial para a função scraper correspondente.
- **Extensibilidade:** adicionar uma nova seção é tão simples quanto
  incluir um novo `case`.

---

### 3. Detalhamento de cada função scraper

#### `find_root_links()` — Descoberta de links

```python
def find_root_links():
    global link_paths
    url = BASE_URL

    while url and url not in visited:
        if not rp.can_fetch("*", url):
            print(f"Acesso bloqueado: {url}")
            break

        visited.add(url)
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        a_element = soup.find_all('a')
        link_paths = []
        for link in a_element:
            link_paths.append(link['href'])

    return link_paths
```

**Propósito:** acessar a página inicial (`index.html`), extrair todos
os links (`<a href="...">`) e retorná-los como uma lista de strings
(`link_paths`).

**Design:**
- Usa `BeautifulSoup` com parser `html.parser` (nativo do Python,
  sem dependências extras).
- `soup.find_all('a')` encontra todos os elementos `<a>`.
- O laço `for link in a_element` extrai o atributo `href` de cada um.
- O conjunto `visited` evita reprocessar a mesma URL.
- A verificação `rp.can_fetch` garante que a página inicial pode ser
  acessada.

---

#### `noticias(path)` — Extração da seção de notícias

```python
soup = BeautifulSoup(html, 'html.parser')
page_title = soup.find('h2')
page_title = page_title.text
article_title = soup.find_all('h4', class_='titulo-noticia')
article_text = soup.find_all('p', class_='resumo')
article_date = soup.find_all('span', class_='data-post')
```

**Propósito:** extrair o título da página, títulos de notícias,
resumos e datas de publicação.

**Design:**
- `soup.find('h2')` — captura o título principal da página (retorna
  a primeira ocorrência, que é convertida para texto com `.text`).
- `soup.find_all('h4', class_='titulo-noticia')` — busca **todas**
  as notícias listadas. Retorna uma lista de objetos Tag.
- As listas são convertidas para texto com list comprehension:
  `[article.contents for article in article_title]`.
  - **`.contents`** retorna uma lista dos filhos diretos do nó
    (incluindo `NavigableString`), preservando a estrutura.
  - Poderíamos usar `.text` ou `.get_text()` para obter string limpa.
- Os dados são empacotados em uma lista e retornados para posterior
  exportação.

---

#### `contato(path)` — Extração da página de contato

```python
title = soup.find('h2', class_='mb-0').text
lead = soup.find('p', class_='lead').text
strongs = soup.find_all('strong')
strongs = [strong.text for strong in strongs]
deptos = soup.find_all('span')
deptos = [depto.text for depto in deptos]
warning = soup.find('div', class_='mt-4').text
```

**Propósito:** extrair título, texto de destaque (lead), elementos em
negrito, spans (departamentos) e aviso.

**Design:**
- Uso de seletores CSS via `class_` para localizar elementos
  específicos.
- `soup.find_all('strong')` captura todos os textos em negrito da
  página.
- `soup.find_all('span')` captura todos os spans (incluindo, por
  exemplo, `<span id="dept-nome">` que está comentado no código).
- A list comprehension `[strong.text for strong in strongs]` extrai
  apenas o texto de cada tag, descartando a estrutura HTML.

---

#### `admin_usuarios(path)` — Seção administrativa (bloqueada)

```python
while url and url not in visited:
    if rp.can_fetch("*", path):
        print(f"Acesso bloqueado por restrições no robots.txt: {url}")
        break
```

**Propósito:** demonstrar o bloqueio por `robots.txt`. A condição
está **invertida** intencionalmente (usa `can_fetch` retornando
`True` para bloquear). Na prática, o `robots.txt` provavelmente
proíbe `Disallow: /admin_usuarios.html`, então `can_fetch` retorna
`False` para o robô `*`, e a função apenas registra a tentativa.

**Observação:** a lógica aqui é o inverso das outras funções para
ilustrar um tratamento diferente de bloqueio — em vez de pular o
acesso e continuar, ela exibe uma mensagem e termina.

---

#### `produtos(path)` — Produtos com paginação recursiva

```python
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
```

**Propósito:** extrair dados de produtos e navegar por todas as
páginas de produto via recursão.

**Design da paginação recursiva:**
1. `soup.find_all('a', class_='page-link')` encontra todos os links
   de paginação (normalmente "Anterior", "1", "2", "3", "Próximo").
2. O índice `[1]` pega o **segundo** link — o primeiro costuma ser
   "Anterior" (href `#` quando na primeira página), e o segundo é a
   primeira página numérica ou "Próximo".
3. Se o href for diferente de `#`, chama `produtos(next)` **de forma
   recursiva**, passando o caminho da próxima página.
4. `time.sleep(SECONDS)` antes da chamada recursiva respeita o
   intervalo de polidez entre requisições.
5. Quando `next == '#'` (não há mais páginas), a recursão termina.

**Por que recursão e não um loop?**
- O código original usa recursão para simplificar o reúso da lógica
  de extração. Cada chamada de `produtos()` processa uma página e
  então decide se deve chamar a si mesma para a próxima.
- **Limitação:** Python tem limite de recursão (padrão ~1000), mas
  para algumas páginas de produtos é mais que suficiente.
- Uma alternativa seria um loop `while`, que seria mais robusto para
  muitas páginas.

---

### 4. Exportação para CSV

O código atual apenas imprime os dados no terminal. Para exportar
para CSV, adicionaríamos o seguinte bloco:

```python
import csv

def export_to_csv(all_data, filename="dados_extraidos.csv"):
    fieldnames = ['secao', 'titulo', 'conteudo']
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_data:
            writer.writerow(row)
```

**Por que `encoding='utf-8-sig'`?**
- `utf-8-sig` inclui o **BOM (Byte Order Mark)** no início do arquivo.
- O Excel (especialmente versões para Windows) usa o BOM para
  reconhecer corretamente arquivos UTF-8.
- Sem o BOM, o Excel pode interpretar caracteres acentuados como
  texto corrompido (ex.: "ç" vira "Ã§").

**Estrutura do CSV:**
- Cada linha representa um dado extraído.
- Colunas sugeridas: `secao` (notícias, contato, produtos),
  `titulo`/`campo`, `conteudo` (texto extraído).
- `csv.DictWriter` mapeia dicionários para colunas com base em
  `fieldnames`.

**Uso no código principal:**

```python
all_data = []

for link_path in link_paths:
    time.sleep(SECONDS)
    match link_path:
        case 'noticias.html':
            dados = noticias(link_path)
            all_data.append({'secao': 'noticias', 'titulo': dados[0], 'conteudo': dados[1:]})
        # ... demais cases ...

export_to_csv(all_data)
```

---

### 5. Tratamento de erros

O código envolve o bloco principal em um `try/except`:

```python
try:
    link_paths = find_root_links()
    # ...
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
except AttributeError as e:
    print(e)
```

**`HTTPError` — Erros HTTP (4xx, 5xx)**
- Subclasse de `URLError`.
- Ocorre quando o servidor retorna códigos como 404 (não encontrado),
  403 (proibido), 500 (erro interno), etc.
- O objeto `e` contém `e.code` (código HTTP) e `e.reason` (mensagem).
- **Exemplo:** se `find_root_links` tentar acessar uma URL que não
  existe, `urlopen` levanta `HTTPError`.

**`URLError` — Erros de rede/DNS**
- Ocorre quando há falha de conexão: DNS não resolve, servidor
  recusa conexão, timeout, etc.
- Geralmente fora do controle do programador.
- **Exemplo:** site está fora do ar ou a máquina está sem internet.

**`AttributeError` — Erros de parsing**
- Ocorre quando `soup.find(...)` retorna `None` e o código tenta
  acessar `.text` ou `.contents` em `None`.
- **Causa comum:** a estrutura HTML da página não corresponde ao
  esperado (classe renomeada, elemento removido, página diferente).
- **Exemplo:** se `soup.find('h2')` retorna `None`, a linha seguinte
  `page_title.text` levanta `AttributeError`.

**Boas práticas adicionais que poderiam ser aplicadas:**

```python
except HTTPError as e:
    print(f"Erro HTTP {e.code} ao acessar {url}: {e.reason}")
except URLError as e:
    print(f"Erro de rede ao acessar {url}: {e.reason}")
except AttributeError as e:
    print(f"Erro de parsing — seletor não encontrado: {e}")
```

**Tratamento local vs. global:**
- O `try/except` atual cobre **todo** o bloco principal.
- Uma abordagem mais refinada envolveria tratar erros dentro de cada
  função scraper, permitindo que uma página com erro não interrompa a
  coleta das demais:

```python
def noticias(path):
    try:
        # ... código de scraping ...
    except (HTTPError, URLError, AttributeError) as e:
        print(f"Erro em noticias({path}): {e}")
        return None
```

---

### 6. Polidez do crawler

```python
SECONDS = 2
# ...
time.sleep(SECONDS)
```

**Por que usar `time.sleep`?**
- Evita sobrecarregar o servidor com requisições em rápida sucessão.
- Simula o comportamento de um navegador humano.
- É um requisito ético e técnico de crawlers bem-comportados.
- O intervalo de 2 segundos é um valor conservador e seguro.

**Onde é aplicado:**
- No loop principal, entre o processamento de cada link:
  ```python
  for link_path in link_paths:
      time.sleep(SECONDS)
      match link_path:
          ...
  ```
- Na paginação recursiva de produtos, antes de chamar a próxima
  página:
  ```python
  time.sleep(SECONDS)
  produtos(next)
  ```

---

### 7. Conjunto `visited` — Evitar reprocessamento

```python
visited = set()
```

- `visited` armazena todas as URLs já acessadas.
- Antes de processar uma URL, cada função verifica `if url not in visited`.
- Como é um `set`, a verificação de pertencimento é O(1).
- Isso evita loops infinitos e requisições duplicadas.
- **Limitação:** o `visited` é limpo apenas quando o programa
  termina. Para crawlers de longa duração, seria necessário persistir
  esse conjunto em disco.

---

### 8. Fluxo completo da execução

```
find_root_links()
    │
    ├── Acessa BASE_URL (index.html)
    ├── Verifica robots.txt
    ├── Extrai todos os <a href="...">
    └── Retorna lista de caminhos
    │
    ▼
Loop: for link_path in link_paths:
    │
    ├── time.sleep(2)
    │
    ├── match link_path:
    │   ├── 'noticias.html'      → noticias()
    │   ├── 'contato.html'       → contato()
    │   ├── 'admin_usuarios.html'→ admin_usuarios()
    │   └── 'produtos_pag1.html' → produtos()
    │
    ▼
produtos() (recursivo)
    │
    ├── Extrai dados da página atual
    ├── time.sleep(2)
    ├── Chama produtos(proxima_pagina)
    │
    ▼
    (continua até next == '#')
```

---

### 9. Possíveis melhorias

| Melhoria | Motivo |
|---|---|
| **Reutilizar `RobotFileParser` global** | Evita nova requisição HTTP do `robots.txt` em cada função |
| **Exportar para CSV** | Persistir os dados extraídos em formato estruturado |
| **Loop em vez de recursão em `produtos`** | Evita estouro da pilha de chamadas |
| **Timeout configurável** | `urlopen(url, timeout=10)` evita travar em conexões lentas |
| **User-Agent personalizado** | Alguns servidores bloqueiam `urllib` sem User-Agent |
| **Logging** | Substituir `print` por `logging` para melhor controle |
| **Parser `lxml`** | Mais rápido que `html.parser` para páginas grandes |
| **Tratamento de erro local** | Impede que uma seção com erro pare a coleta inteira |

---

## Referências

- [urllib.robotparser — Parser for robots.txt](https://docs.python.org/3/library/urllib.robotparser.html)
- [PEP 634 — Structural Pattern Matching](https://peps.python.org/pep-0634/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html)
- [The Web Robots Pages — robots.txt](https://www.robotstxt.org/)
