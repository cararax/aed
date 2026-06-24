# Python — Guia de Ambientação

> 🐍 **Foco**: Fundamentos da linguagem Python para Análise de Dados
> Baseado nos slides: [`02 - Ambientacao Python/`](../02%20-%20Ambientacao%20Python/)

---

## Sumário

- [Quick Reference](#1-quick-reference)
- [Guia Detalhado](#2-guia-detalhado)
  - [1. Características da Linguagem](#1-características-da-linguagem)
  - [2. Tipos de Dados](#2-tipos-de-dados)
  - [3. Conversão de Tipos](#3-conversão-de-tipos)
  - [4. Operadores Matemáticos](#4-operadores-matemáticos)
  - [5. Módulos (import)](#5-módulos-import)
  - [6. Entrada e Saída (input/print)](#6-entrada-e-saída-inputprint)
  - [7. Condicionais (if/elif/else)](#7-condicionais-ifelifelse)
  - [8. Laços (while/for)](#8-laços-whilefor)
  - [9. Funções (def)](#9-funções-def)
  - [10. Strings](#10-strings)
  - [11. Listas](#11-listas)
  - [12. Tuplas](#12-tuplas)
  - [13. Dicionários](#13-dicionários)
  - [14. Tratamento de Exceções (try/except)](#14-tratamento-de-exceções-tryexcept)
  - [15. Estruturas Aninhadas](#15-estruturas-aninhadas)
- [Exercícios](#3-exercícios)

---

## 1. Quick Reference

### Tipos de Dados

| Tipo | Exemplo | Função Conversão |
|------|---------|-----------------|
| `int` | `42` | `int()` |
| `float` | `3.14` | `float()` |
| `str` | `"Python"` | `str()` |
| `bool` | `True` / `False` | `bool()` |
| `complex` | `3+4j` | `complex()` |

### Operadores Matemáticos

| Operador | Significado | Exemplo | Resultado |
|----------|-------------|---------|-----------|
| `+` | Soma | `10 + 3` | `13` |
| `-` | Subtração | `10 - 3` | `7` |
| `*` | Multiplicação | `10 * 3` | `30` |
| `/` | Divisão real | `10 / 3` | `3.333...` |
| `//` | Divisão inteira | `10 // 3` | `3` |
| `%` | Módulo (resto) | `10 % 3` | `1` |
| `**` | Potência | `10 ** 3` | `1000` |

### Operadores de Comparação

`==` `!=` `<` `>` `<=` `>=`

### Operadores Lógicos

`and` `or` `not`

### Operadores Especiais

| Operador | Uso | Exemplo |
|----------|-----|---------|
| `is` | Identidade (mesmo objeto) | `x is None` |
| `in` | Pertinência | `"a" in "abc"` |

### Métodos de String

| Método | O que faz |
|--------|-----------|
| `.upper()` | Maiúsculas |
| `.lower()` | Minúsculas |
| `.find(s)` | Posição da substring (ou -1) |
| `.count(s)` | Quantas vezes aparece |
| `.split(sep)` | Divide em lista |
| `.strip()` | Remove espaços nas bordas |

### Métodos de Lista

| Método | O que faz |
|--------|-----------|
| `.append(x)` | Adiciona ao final |
| `.remove(x)` | Remove primeira ocorrência |
| `.insert(i, x)` | Insere na posição i |
| `.pop(i)` | Remove e retorna elemento |
| `.sort()` | Ordena in-place |
| `.extend(lista)` | Estende com outra lista |

### Métodos de Dicionário

| Método | O que faz |
|--------|-----------|
| `.items()` | Pares (chave, valor) |
| `.keys()` | Lista de chaves |
| `.values()` | Lista de valores |
| `.get(chave)` | Retorna valor ou None |
| `.pop(chave)` | Remove e retorna valor |

### Estruturas de Controle

```python
# if / elif / else
if condicao:
    ...
elif outra:
    ...
else:
    ...

# while
while condicao:
    ...

# for com range
for i in range(inicio, fim, passo):
    ...

# for em coleção
for item in lista:
    ...

# break / continue
break   # sai do laço
continue  # pula para próxima iteração
```

### Tratamento de Exceções

```python
try:
    # código perigoso
except TipoErro as e:
    # tratamento
else:
    # executa se não houve erro
finally:
    # executa sempre
```

---

## 2. Guia Detalhado

### 1. Características da Linguagem

- **Interpretada**: o código é executado linha a linha, sem necessidade de compilação
- **Tipagem dinâmica**: a variável assume o tipo do valor atribuído — não precisa declarar
- **Indentação obrigatória**: define blocos de código (em vez de `{}` ou `begin/end`)
- **Case-sensitive**: `nome` e `Nome` são variáveis diferentes

```python
# Tipagem dinâmica
x = 10        # int
x = "texto"   # str — mesma variável, novo tipo

# Indentação define blocos
if x == 10:
    print("dentro do if")    # 4 espaços (ou 1 tab)
```

### 2. Tipos de Dados

```python
idade = 25           # int
preco = 19.99        # float
nome = "João"        # str
ativo = True         # bool
complexo = 3 + 4j    # complex

print(type(idade))   # <class 'int'>
print(type(preco))   # <class 'float'>
```

### 3. Conversão de Tipos

```python
# Conversões explícitas
int("42")         # 42
float("3.14")     # 3.14
str(42)           # "42"
int(3.99)         # 3  (trunca, não arredonda)

# Cuidado: conversão inválida gera erro
# int("abc") → ValueError
```

### 4. Operadores Matemáticos

```python
print(10 + 3)     # 13
print(10 - 3)     # 7
print(10 * 3)     # 30
print(10 / 3)     # 3.3333333333333335  (divisão real)
print(10 // 3)    # 3   (divisão inteira)
print(10 % 3)     # 1   (resto da divisão)
print(10 ** 3)    # 1000  (potência)

# Precedência: ** > *, /, //, % > +, -
print(2 + 3 * 4)   # 14
print((2 + 3) * 4) # 20
```

### 5. Módulos (import)

```python
# Importar módulo completo
import math
print(math.sqrt(16))    # 4.0

# Importar função específica
from math import sqrt
print(sqrt(16))         # 4.0

# Importar com apelido
import math as m
print(m.sqrt(16))       # 4.0

# Importar várias funções
from math import sqrt, pi
print(sqrt(25))         # 5.0
print(pi)               # 3.141592653589793

# Outros módulos úteis: random, datetime, os, sys
```

### 6. Entrada e Saída (input/print)

```python
# input() sempre retorna string
nome = input("Digite seu nome: ")

# Converter para número
idade = int(input("Digite sua idade: "))

# print básico
print("Olá", nome)

# f-strings (Python 3.6+)
print(f"Olá {nome}, você tem {idade} anos")

# Formatação numérica
preco = 19.9905
print(f"Preço: R${preco:.2f}")   # Preço: R$19.99
print(f"{preco:10.2f}")          # Alinhamento à direita

# Formatação estilo C (%)
print("Valor: %.2f" % preco)
```

### 7. Condicionais (if/elif/else)

```python
# Estrutura básica
if idade >= 18:
    print("Maior de idade")
elif idade >= 16:
    print("Pode votar")
else:
    print("Menor de idade")

# Operadores lógicos
if idade >= 18 and possui_carteira:
    print("Pode dirigir")

if idade < 16 or not autorizado:
    print("Não pode entrar")

# Operador is (identidade)
if x is None:
    print("x é None")

# Operador in (pertinência)
if "joão" in nomes:
    print("João está na lista")
```

### 8. Laços (while/for)

#### while

```python
# Repete enquanto condição for verdadeira
contador = 0
while contador < 5:
    print(contador)
    contador += 1
# Saída: 0 1 2 3 4

# while com flag
flag = False
while not flag:
    valor = int(input("Digite: "))
    if valor < 0:
        flag = True
```

#### for com range

```python
# range(fim) → 0 até fim-1
for i in range(5):
    print(i)          # 0 1 2 3 4

# range(inicio, fim)
for i in range(2, 6):
    print(i)          # 2 3 4 5

# range(inicio, fim, passo)
for i in range(0, 10, 2):
    print(i)          # 0 2 4 6 8
```

#### for em coleções

```python
lista = ["a", "b", "c"]
for item in lista:
    print(item)       # a b c

# enumerate — índice e valor
for i, item in enumerate(lista):
    print(i, item)    # 0 a / 1 b / 2 c
```

#### break / continue / else no laço

```python
# break — interrompe o laço
for i in range(10):
    if i == 5:
        break
    print(i)          # 0 1 2 3 4

# continue — pula para próxima iteração
for i in range(5):
    if i == 2:
        continue
    print(i)          # 0 1 3 4

# else no for — executa se NÃO houve break
for i in range(3):
    print(i)
else:
    print("Laço completou sem break")  # executa
```

### 9. Funções (def)

```python
# Função simples
def saudacao():
    print("Olá!")

saudacao()    # Olá!

# Parâmetros e retorno
def somar(a, b):
    return a + b

resultado = somar(3, 4)
print(resultado)  # 7

# Parâmetro default
def saudacao(nome, saudacao="Olá"):
    print(f"{saudacao}, {nome}!")

saudacao("João")            # Olá, João!
saudacao("Maria", "Oi")     # Oi, Maria!

# *args — número variável de argumentos posicionais
def somar_todos(*args):
    return sum(args)

print(somar_todos(1, 2, 3, 4))  # 10

# **kwargs — número variável de argumentos nomeados
def exibir_dados(**kwargs):
    for chave, valor in kwargs.items():
        print(f"{chave}: {valor}")

exibir_dados(nome="João", idade=30)
# nome: João
# idade: 30
```

### 10. Strings

```python
texto = "Python para Análise de Dados"

# Acesso por índice
print(texto[0])      # P
print(texto[-1])     # s

# Fatiamento (slicing) — [inicio:fim:passo]
print(texto[0:6])    # Python
print(texto[:6])     # Python (mesmo que acima)
print(texto[7:])     # para Análise de Dados
print(texto[::-1])   # Inverte a string

# Métodos
print(texto.upper())              # PYTHON PARA ANÁLISE DE DADOS
print(texto.lower())              # python para análise de dados
print(texto.find("Análise"))      # 13
print(texto.find("SQL"))          # -1 (não encontrou)
print(texto.count("a"))           # 4
print(texto.split())              # ['Python', 'para', 'Análise', 'de', 'Dados']
print(texto.split("a"))           # ['Python p', 'r', ' Análise de D', 'dos']

# split com log
log = '192.168.0.1 - - [03/Mar/2026:10:15:32] "GET /produtos HTTP/1.1" 200 532'
partes = log.split()
print(partes[0])      # 192.168.0.1
```

### 11. Listas

```python
# Criação
numeros = [1, 2, 3, 4, 5]
compras = ["leite", "pão", "ovos"]
misturada = [1, "texto", True, 3.14]

# Listas são mutáveis
compras[0] = "iogurte"

# Métodos principais
compras = ["leite", "pão", "ovos"]

compras.append("queijo")
print(compras)          # ['leite', 'pão', 'ovos', 'queijo']

compras.remove("pão")
print(compras)          # ['leite', 'ovos', 'queijo']

compras.insert(0, "iogurte")
print(compras)          # ['iogurte', 'leite', 'ovos', 'queijo']

ultimo = compras.pop()
print(ultimo)           # queijo
print(compras)          # ['iogurte', 'leite', 'ovos']

# Ordenação
valores = [3, 1, 4, 1, 5]
valores.sort()
print(valores)          # [1, 1, 3, 4, 5]

# Soma, média
temperaturas = [25.5, 27.0, 26.5, 25.5, 28.1, 25.5]
print(sum(temperaturas))          # 158.1
print(sum(temperaturas) / 6)      # 26.35
print(temperaturas.count(25.5))   # 3
```

### 12. Tuplas

```python
# Criação
ponto = (10, 20)

# Acesso por índice
print(ponto[0])        # 10

# Tuplas são IMUTÁVEIS — não podem ser alteradas
# ponto[0] = 30       # TypeError!

# Métodos
print(ponto.count(10))  # 1
print(ponto.index(20))  # 1

# Conversão tupla → lista
numeros_impares = (1, 3, 5, 7)
lista_impares = list(numeros_impares)
print(lista_impares)    # [1, 3, 5, 7]

# Combinar listas
pares = [2, 4, 6, 8]
completos = pares + lista_impares
completos.sort()
print(completos)        # [1, 2, 3, 4, 5, 6, 7, 8]
```

### 13. Dicionários

```python
# Criação
dados = {
    "nome": "João",
    "idade": 30,
    "telefone": "9999-9999"
}

# Acesso
print(dados["nome"])       # João

# get() — seguro (retorna None se chave não existe)
print(dados.get("email"))           # None
print(dados.get("email", "N/A"))    # "N/A"

# Adicionar/alterar
dados["endereco"] = "Rua A, 123"

# Iteração
for chave, valor in dados.items():
    print(f"{chave}: {valor}")

# Apenas chaves ou valores
print(dados.keys())     # dict_keys(['nome', 'idade', 'telefone', 'endereco'])
print(dados.values())   # dict_values(['João', 30, '9999-9999', 'Rua A, 123'])

# pop() — remove e retorna
email = dados.pop("telefone")
print(email)            # 9999-9999
```

### 14. Tratamento de Exceções (try/except)

```python
# Estrutura completa
try:
    valor = int(input("Digite um número: "))
    resultado = 10 / valor
except ValueError:
    print("Erro: digite um número válido")
except ZeroDivisionError:
    print("Erro: divisão por zero")
except Exception as e:
    print(f"Erro inesperado: {e}")
else:
    print(f"Resultado: {resultado}")   # executa se NÃO houve erro
finally:
    print("Fim do programa")            # executa SEMPRE

# raise — lançar exceção propositalmente
def dividir(a, b):
    if b == 0:
        raise ValueError("Divisor não pode ser zero")
    return a / b

try:
    print(dividir(10, 0))
except ValueError as e:
    print(e)              # Divisor não pode ser zero
```

### 15. Estruturas Aninhadas

```python
# Lista de tuplas — catálogo de produtos
catalogo = [
    ("meia", 10.00),
    ("camiseta", 55.90),
    ("calça", 120.00)
]

# Acessar segundo produto
print(catalogo[1])             # ('camiseta', 55.90)
print(catalogo[1][0])          # camiseta

# Adicionar produto
catalogo.append(("computador", 5000.00))

# Percorrer
for nome, preco in catalogo:
    print(f"Produto: {nome} - Preço: R${preco:.2f}")

# Lista de dicionários — agenda de contatos
agenda = [
    {"nome": "João", "telefone": "1111-1111"},
    {"nome": "Maria", "telefone": "2222-2222"},
    {"nome": "Pedro", "telefone": "3333-3333"}
]

# Acessar dados
print(agenda[0]["nome"])       # João

# Iterar
for contato in agenda:
    print(f"{contato['nome']}: {contato['telefone']}")

# Dicionário com listas
contagem = {"Sucesso": 0, "Erro": 0, "Redirecionamento": 0}
status_codes = [200, 404, 500, 301, 200, 403, 502, 200]
for code in status_codes:
    if 200 <= code <= 299:
        contagem["Sucesso"] += 1
    elif 400 <= code <= 499:
        contagem["Erro"] += 1
print(contagem)   # {'Sucesso': 3, 'Erro': 2, 'Redirecionamento': 1}
```

---

## 3. Exercícios

### Exercícios Aula 1

Arquivo original: [`05 - Exercicios Aula 1/`](../02%20-%20Ambientacao%20Python/05%20-%20Exercicios%20Aula%201/)

| # | Enunciado | Conceitos |
|---|-----------|-----------|
| 1 | Ler valor do produto e forma de pagamento, calcular desconto/juros | `input`, `if/elif/else`, `float` |
| 2 | Ler pares de valores até que o primeiro seja menor que o segundo | `while`, `input`, `int` |
| 3 | Ler valores maiores que o anterior, com condição de parada | `while`, `flag`, `if` |
| 4 | Verificar se número é perfeito (soma dos divisores) | `for`, `range`, `if`, função |
| 5 | Calcular duração de jogo com horas/minutos (pode virar o dia) | `if`, `//`, `%`, `datetime` |

📍 **Resolução**: [Exercícios Aula 1](resolucoes/01%20-%20resolucao%20-%20exercicios%20aula%201.md)

### Tuplas, Listas e Dicionários

Arquivo original: [`06 - Exercicios - Tuplas Listas Dicionarios/`](../02%20-%20Ambientacao%20Python/06%20-%20Exercicios%20-%20Tuplas%20Listas%20Dicionarios/)

| # | Enunciado | Conceitos |
|---|-----------|-----------|
| 1 | Manipular lista de compras (append, remove, insert) | `list.append`, `list.remove`, `list.insert` |
| 2 | Acessar coordenada em tupla, tentar modificar (erro) | Tupla imutável, `tuple[index]` |
| 3 | Converter tupla para lista, combinar e ordenar | `list()`, `+`, `list.sort()` |
| 4 | Calcular média e contar ocorrências em lista | `sum()`, `len()`, `list.count()` |
| 5 | Lista de tuplas como catálogo de produtos | Lista de tuplas, `for` com unpack |
| 6 | Dicionário com dados pessoais e iteração | `dict.items()`, `for` |
| 7 | Agenda com dicionários — ler dados e imprimir | `dict`, laço, `input` |

📍 **Resolução**: [Tuplas Listas Dicionários](resolucoes/02%20-%20resolucao%20-%20tuplas%20listas%20dicionarios.md)

### Desafios Ambientação

Arquivo original: [`07 - Desafios - Ambientacao Python.docx`](../02%20-%20Ambientacao%20Python/07%20-%20Desafios%20-%20Ambientacao%20Python.docx)

| # | Enunciado | Conceitos |
|---|-----------|-----------|
| 1 | Extrair campos de um log HTTP (IP, método, URL, status) | `split`, `find`, slicing de string |
| 2 | Classificar status codes HTTP com dicionário de contagem | `if/elif`, `dict`, `for` |
| 3 | Analisar acessos a URLs (contagem, erros, URLs únicas) | Lista de tuplas, `dict`, `for`, `if` |
| 4 | Simular tentativas de acesso com tratamento de exceções | `try/except/else/finally`, `raise`, `for` |

📍 **Resolução**: [Desafios Ambientação](resolucoes/03%20-%20resolucao%20-%20desafios%20ambientacao.md)

---

> 📎 **Slides originais**:
> - [Slides Python Parte 1](../02%20-%20Ambientacao%20Python/01%20-%20Slides%20-%20Python%20Parte%201.pptx)
> - [Slides Python Parte 2 — Input, If, Laços, Funções](../02%20-%20Ambientacao%20Python/02%20-%20Slides%20-%20Python%20Parte%202%20-%20Input%20If%20Lacos%20Funcoes.pptx)
> - [Slides Python Parte 3 — Tuplas, Listas, Dicionários](../02%20-%20Ambientacao%20Python/03%20-%20Slides%20-%20Python%20Parte%203%20-%20Tuplas%20Listas%20Dicionarios.pptx)
> - [Slides Python Parte 4 — Tratamento de Exceções](../02%20-%20Ambientacao%20Python/04%20-%20Slides%20-%20Python%20Parte%204%20-%20Tratamento%20Excecoes.pptx)
> 📚 **Material de apoio**: [`00 - Materiais De Apoio/03 - Python Para Todos - Severance.pdf`](../00%20-%20Materiais%20De%20Apoio/03%20-%20Python%20Para%20Todos%20-%20Severance.pdf)
