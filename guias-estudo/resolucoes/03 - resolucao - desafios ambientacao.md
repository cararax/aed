# Resolução — Desafios Ambientação Python

---

## Sumário

- [Desafio 1 — Parse de linha de log Apache](#desafio-1)
- [Desafio 2 — Classificação de códigos HTTP](#desafio-2)
- [Desafio 3 — Contagem de acessos a URLs](#desafio-3)
- [Desafio 4 — Validação de entrada com try/except](#desafio-4)

---

## Desafio 1

**Enunciado:**  
Extrair de uma linha de log Apache o IP, método HTTP, URL, status code e
tamanho da resposta **sem usar regex** — apenas `split()`, `find()` e slicing.

```
Linha: 192.168.0.10 - - [03/Mar/2026:10:15:32] "GET /produtos?id=10 HTTP/1.1" 200 532
```

**Por que usar split / find / slicing em vez de regex?**

1. A linha tem estrutura previsível e simples — não precisamos da
   flexibilidade (e complexidade) de uma expressão regular.
2. `split()` quebra por espaços; o IP é o primeiro campo.
3. `find()` localiza aspas; slicing extrai a requisição entre elas.
4. Regex seria **mais frágil** neste caso (escapar caracteres,
   grupos de captura, etc.) e mais lenta para um parse simples.

```python
log = '192.168.0.10 - - [03/Mar/2026:10:15:32] "GET /produtos?id=10 HTTP/1.1" 200 532'

# split() — quebra a string em listas de palavras
# -------------------------------------------------
# Por padrão, split() separa por qualquer quantidade de
# espaços em branco. Cada palavra vira um elemento da lista.
# Resultado: ['192.168.0.10', '-', '-', '[03/Mar/2026:10:15:32]',
#             '"GET', '/produtos?id=10', 'HTTP/1.1"', '200', '532']
partes = log.split()

# O IP é sempre o PRIMEIRO campo da linha de log Apache.
# partes[0] = '192.168.0.10'
ip = partes[0]

# A requisição HTTP está entre aspas duplas.
# Precisamos achar ONDE as aspas estão para extrair o interior.
# find('"') retorna o ÍNDICE (posição) da primeira aspa na string.
indice_inicio = log.find('"')

# find() com segundo argumento — busca a partir de uma posição
# -------------------------------------------------------------
# log.find('"', indice_inicio + 1) começa a procurar LOGO APÓS
# a primeira aspa, encontrando a aspa de fechamento.
indice_fim = log.find('"', indice_inicio + 1)

# Slicing — extraindo substring entre as aspas
# ---------------------------------------------
# log[indice_inicio + 1 : indice_fim] pega tudo DEPOIS da
# primeira aspa (excluindo ela) ATÉ a segunda aspa (excluindo ela).
# Resultado: 'GET /produtos?id=10 HTTP/1.1'
requisicao = log[indice_inicio + 1 : indice_fim]

# A requisição também é separada por espaços — split() novamente.
# Como temos exatamente 3 campos, podemos desempacotar em
# 3 variáveis de uma vez (tuple unpacking).
# 'GET /produtos?id=10 HTTP/1.1' → ['GET', '/produtos?id=10', 'HTTP/1.1']
metodo, url, protocolo = requisicao.split()

# Posições FIXAS no final da linha original
# -------------------------------------------
# O status code está na penúltima posição da lista original.
# partes[-2] = '200' (segundo de trás para frente)
status = partes[-2]

# O tamanho está na última posição.
# partes[-1] = '532' (último elemento)
tamanho = partes[-1]

print(f"IP: {ip}")
print(f"Método: {metodo}")
print(f"URL: {url}")
print(f"Status: {status}")
print(f"Tamanho da resposta: {tamanho} bytes")
```

---

## Desafio 2

**Enunciado:**  
Classificar uma lista de códigos HTTP em categorias usando uma função
e um dicionário para contagem.

```
status_codes = [200, 404, 500, 301, 403, 200, 502, 201]
```

| Categoria            | Faixa       |
|----------------------|-------------|
| Sucesso              | 200–299     |
| Redirecionamento     | 300–399     |
| Erro do Cliente      | 400–499     |
| Erro do Servidor     | 500–599     |
| Desconhecido         | outros      |

**Padrão: função + dicionário**

1. Uma função **pura** (só depende dos argumentos, sem efeitos colaterais)
   mapeia código → categoria.
2. Um dicionário armazena a contagem de cada categoria.
3. Iteramos pela lista, classificamos cada código e incrementamos.

```python
status_codes = [200, 404, 500, 301, 403, 200, 502, 201]

# Definindo a função classificadora
# -----------------------------------
# def classificar_status(code):
#     if 200 <= code <= 299:   # Python permite comparar em cadeia!
#         return "Sucesso"
#     elif 300 <= code <= 399:
#         ...
#     else:
#         return "Desconhecido"
#
# Por que if/elif/else encadeado?
# - Apenas UMA categoria se aplica a cada código.
# - O primeiro return encerra a função — os elif seguintes
#   só executam se o anterior for False.
# - O else final captura qualquer valor fora das faixas.
#
# Nota: 200 <= code <= 299 é uma COMPARAÇÃO EM CADEIA do Python
# equivalente a code >= 200 and code <= 299. Mais legível.

def classificar_status(code):
    if 200 <= code <= 299:
        return "Sucesso"
    elif 300 <= code <= 399:
        return "Redirecionamento"
    elif 400 <= code <= 499:
        return "Erro do Cliente"
    elif 500 <= code <= 599:
        return "Erro do Servidor"
    else:
        return "Desconhecido"

# Inicializando o dicionário de contagem
# ---------------------------------------
# Precisamos de uma entrada para cada categoria ANTES de incrementar.
# Se tentarmos fazer contagem[categoria] += 1 sem a chave existir,
# lançará KeyError.
#
# Abordagem: dicionário com todas as categorias zeradas.
# Alternativa (ver desafio 3): dict vazio + if chave in dict.
contagem = {
    "Sucesso": 0,
    "Redirecionamento": 0,
    "Erro do Cliente": 0,
    "Erro do Servidor": 0,
    "Desconhecido": 0
}

# Loop de classificação
# ----------------------
# Para cada code em status_codes:
#   1. Chama classificar_status(code) → retorna string da categoria
#   2. Usa a string como chave do dicionário
#   3. Incrementa o valor (que já existe, garantido pela inicialização)
for code in status_codes:
    categoria = classificar_status(code)
    contagem[categoria] += 1

print("Relatório:")
for categoria, quantidade in contagem.items():
    print(f"{categoria}: {quantidade}")

# Saída esperada:
# Sucesso: 3
# Redirecionamento: 1
# Erro do Cliente: 2
# Erro do Servidor: 2
# Desconhecido: 0
```

---

## Desafio 3

**Enunciado:**  
A partir de uma lista de tuplas (url, status), contar quantas vezes
cada URL foi acessada, identificar a URL mais acessada e quantos
erros (status >= 400) ocorreram.

```python
acessos = [
    ("/home", 200), ("/produtos", 200), ("/home", 200),
    ("/login", 403), ("/produtos", 200), ("/carrinho", 500), ("/home", 200)
]
```

**Padrão de contagem em dicionário**

Há duas abordagens comuns:

| Abordagem | Código | Comportamento |
|-----------|--------|---------------|
| `if` + `in` | `if url in contagem: contagem[url] += 1 else: contagem[url] = 1` | Verifica existência antes de incrementar |
| `.setdefault()` | `contagem.setdefault(url, 0); contagem[url] += 1` | Se não existir, insere com valor 0, depois incrementa |

Ambas funcionam. A primeira é mais explícita; a segunda é mais concisa.

```python
acessos = [
    ("/home", 200),
    ("/produtos", 200),
    ("/home", 200),
    ("/login", 403),
    ("/produtos", 200),
    ("/carrinho", 500),
    ("/home", 200)
]

contagem_urls = {}
total_erros = 0

# Percorrendo a lista de acessos
# -------------------------------
# Cada elemento é uma tupla (url, status).
# Podemos "desempacotar" diretamente no for:
# for url, status in acessos:
# Isso atribui url = acessos[i][0], status = acessos[i][1].
for url, status in acessos:

    # Contagem de URLs — padrão if/else
    # -----------------------------------
    # if url in contagem_urls:
    #     A chave já existe → incrementa.
    # else:
    #     Primeira vez que vemos esta URL → cria chave com valor 1.
    #
    # Por que não inicializar o dict com as URLs de antemão?
    # Porque nem sempre sabemos quais URLs aparecerão.
    if url in contagem_urls:
        contagem_urls[url] += 1
    else:
        contagem_urls[url] = 1

    # Contagem de erros (status >= 400)
    # ----------------------------------
    # Códigos 4xx = erro do cliente, 5xx = erro do servidor.
    # Ambos indicam falha na requisição.
    if status >= 400:
        total_erros += 1

# Encontrando a URL mais acessada
# --------------------------------
# Estratégia: percorrer o dicionário e manter o MAIOR valor visto.
#
# url_mais_acessada = None  → ainda não encontramos nenhuma
# maior_valor = 0           → qualquer valor positivo é maior
#
# Alternativa: max(contagem_urls, key=contagem_urls.get)
# Mas o loop explícito é mais didático.
url_mais_acessada = None
maior_valor = 0

# .items() retorna pares (chave, valor)
# Comparamos valor com maior_valor; se for maior, atualizamos.
for url, quantidade in contagem_urls.items():
    if quantidade > maior_valor:
        maior_valor = quantidade
        url_mais_acessada = url

# .keys() retorna uma visão das chaves — convertemos para lista
urls_unicas = list(contagem_urls.keys())

print("Contagem por URL:", contagem_urls)
print("URL mais acessada:", url_mais_acessada)
print("Total de erros:", total_erros)
print("URLs únicas:", urls_unicas)

# Saída esperada:
# Contagem por URL: {'/home': 3, '/produtos': 2, '/login': 1, '/carrinho': 1}
# URL mais acessada: /home
# Total de erros: 2
# URLs únicas: ['/home', '/produtos', '/login', '/carrinho']
```

---

## Desafio 4

**Enunciado:**  
Usar `try/except` para validar entrada do usuário, tratando
`ValueError` (conversão inválida), `ZeroDivisionError` (divisão
por zero), com blocos `else` e `finally`.

**Ordem dos except blocks**

- `except ValueError` **antes** de `except Exception`
- `except ZeroDivisionError` **antes** de `except Exception`
- `except Exception` por último (captura qualquer erro não previsto)

```
try:
    bloco arriscado
except ValueError:
    erro de conversão / valor inválido
except ZeroDivisionError:
    divisão por zero
except Exception:
    qualquer outro erro (genérico)
else:
    executa se NENHUM except foi acionado
finally:
    executa SEMPRE, com ou sem erro
```

**else vs finally**

| Bloco    | Executa quando?                                    |
|----------|----------------------------------------------------|
| `else`   | Só executa se **nenhuma** exceção foi levantada. |
| `finally`| Executa **sempre** — haja erro ou não.             |

```python
# try — bloco principal onde erros podem ocorrer
# ------------------------------------------------
try:
    # input() sempre retorna string.
    # Se o usuário digitar algo que não pode ser convertido
    # para int, int() lança ValueError.
    url = input("Digite a URL: ")
    tentativas = int(input("Digite o número de tentativas: "))

    # raise — levantando exceção manualmente
    # ----------------------------------------
    # Aqui nós DECIDIMOS que tentativas <= 0 é inválido.
    # raise dispara uma exceção que pode ser capturada
    # por um except mais acima.
    if tentativas <= 0:
        raise ValueError("Número de tentativas deve ser maior que zero.")

    for i in range(tentativas):
        print(f"Tentativa {i + 1} de acessar {url}")

        # Divisão proposital para causar ZeroDivisionError
        # --------------------------------------------------
        # range(tentativas) vai de 0 a tentativas-1.
        # Na última iteração, tentativas - i - 1 == 0.
        # 10 / 0 → ZeroDivisionError
        resultado = 10 / (tentativas - i - 1)

# except captura erros ESPECÍFICOS
# ----------------------------------
# A ORDEM dos except importa! O Python testa de cima para baixo
# e executa o PRIMEIRO que casa com o tipo da exceção.
#
# Regra: colocar exceções MAIS ESPECÍFICAS primeiro,
#        exceções MAIS GENÉRICAS por último.
#
#             ValueError e ZeroDivisionError são subclasses de Exception.
#   Se colocássemos except Exception primeiro, ele capturaria TUDO
#   e os except específicos nunca executariam.

# ValueError — captura erro de conversão int() ou raise manual
except ValueError as e:
    # "as e" vincula a exceção à variável 'e' para exibir a mensagem
    print("Erro de valor:", e)

# ZeroDivisionError — captura divisão por zero
except ZeroDivisionError:
    print("Erro: divisão por zero ocorreu durante simulação.")

# Exception — captura QUALQUER outra exceção não prevista
# (segurança: evita que o programa quebre com erros inesperados)
except Exception as e:
    print("Erro inesperado:", e)

# else — executado SOMENTE se NENHUM except foi acionado
# -------------------------------------------------------
# Cuidado: else NÃO executa se houve exceção.
# Útil para código que só deve rodar se tudo deu certo.
else:
    print("Execução concluída sem erros.")

# finally — executado SEMPRE, haja erro ou não
# ---------------------------------------------
# Usado para ações de limpeza: fechar arquivos, encerrar
# conexões de rede, liberar recursos, etc.
# Mesmo que haja um return no try, o finally executa antes.
finally:
    print("Encerrando programa.")
```

---
