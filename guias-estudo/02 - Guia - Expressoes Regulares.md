# Expressões Regulares — Guia de Estudo

> Abrange Regex teórico + Regex com Python, baseado nos slides e listas das pastas [`03 - Regex/`](../03%20-%20Regex/) e [`04 - Regex Com Python/`](../04%20-%20Regex%20Com%20Python/).

---

## Sumário

- [Quick Reference](#1-quick-reference)
  - [Metacaracteres Regex](#metacaracteres-regex)
  - [Shorthands](#shorthands)
  - [Quantificadores](#quantificadores)
  - [Âncoras](#âncoras)
  - [Grupos](#grupos)
  - [Funções `re` do Python](#funções-re-do-python)
  - [Flags](#flags)
  - [Métodos do Match Object](#métodos-do-match-object)
- [Guia Detalhado](#2-guia-detalhado)
  - [1. Metacaracteres Básicos](#1-metacaracteres-básicos)
  - [2. Shorthands](#2-shorthands)
  - [3. Quantificadores](#3-quantificadores)
  - [4. Âncoras](#4-âncoras)
  - [5. Grupos e Backreferences](#5-grupos-e-backreferences)
  - [6. Alternação](#6-alternação)
  - [7. Escape](#7-escape)
  - [8. Wildcard `.*`](#8-wildcard-)
  - [9. Greedy vs Lazy](#9-greedy-vs-lazy)
  - [10. Funções re.xxx](#10-funções-rexxx)
  - [11. Flags](#11-flags)
  - [12. Match Object](#12-match-object)
  - [13. Named Groups com `groupdict()`](#13-named-groups-com-groupdict)
- [Exercícios](#3-exercícios)

---

## 1. Quick Reference

### Metacaracteres Regex

| Meta | Nome | O que faz | Exemplo | Match |
|------|------|-----------|---------|-------|
| `.` | Ponto (dot) | Qualquer caractere (exceto quebra de linha) | `c.t` | `cat`, `cut`, `c4t` |
| `[abc]` | Classe de caracteres | Um dos caracteres listados | `[aeiou]` | Qualquer vogal |
| `[a-z]` | Classe com intervalo | Qualquer letra minúscula | `[0-9]` | Qualquer dígito |
| `[^abc]` | Classe negada | Nenhum dos caracteres listados | `[^0-9]` | Qualquer não-dígito |

### Shorthands

| Shorthand | Significa | Equivale a | Match |
|-----------|-----------|------------|-------|
| `\d` | Dígito | `[0-9]` | `5`, `0`, `9` |
| `\D` | Não-dígito | `[^0-9]` | `a`, `$`, espaço |
| `\w` | Word char (letra/dígito/`_`) | `[a-zA-Z0-9_]` | `a`, `Z`, `3`, `_` |
| `\W` | Não-word char | `[^a-zA-Z0-9_]` | `@`, `-`, espaço |
| `\s` | Whitespace | `[ \t\n\r\f\v]` | Espaço, tab, newline |
| `\S` | Não-whitespace | `[^ \t\n\r\f\v]` | `a`, `5`, `@` |

### Quantificadores

| Quant | O que faz | Exemplo | Match |
|-------|-----------|---------|-------|
| `?` | Zero ou um (opcional) | `colou?r` | `color`, `colour` |
| `*` | Zero ou mais | `ab*c` | `ac`, `abc`, `abbc`, … |
| `+` | Um ou mais | `ab+c` | `abc`, `abbc` (não `ac`) |
| `{n}` | Exatamente n | `\d{3}` | `123`, `999` |
| `{n,m}` | De n a m | `\d{2,4}` | `12`, `123`, `1234` |
| `{n,}` | n ou mais | `\d{3,}` | `123`, `12345` |
| `*?`, `+?`, `??` | Versões **lazy** (mínimo possível) | `a.*?b` | `a...b` (menor match) |

### Âncoras

| Âncora | O que faz | Exemplo | Match |
|--------|-----------|---------|-------|
| `^` | Início da string/linha | `^Python` | `Python é...` |
| `$` | Fim da string/linha | `fim$` | `...é o fim` |
| `\b` | Fronteira de palavra | `\bword\b` | `word` (não `sword`) |
| `\B` | Não-fronteira de palavra | `\Bword` | `sword` (não `word `) |

### Grupos

| Sintaxe | O que faz | Exemplo |
|---------|-----------|---------|
| `(...)` | Grupo de captura | `(\d{2})/(\d{2})` |
| `\1` .. `\9` | Backreference | `(\w)\1` → `aa`, `bb` |
| `(?:...)` | Grupo não-capturante | `(?:sim|não)` |
| `(?P<nome>...)` | Grupo nomeado | `(?P<ano>\d{4})` |

### Funções `re` do Python

| Função | Retorna | Uso típico |
|--------|---------|------------|
| `re.search(padrão, texto)` | Match object (1º match) ou `None` | "Existe o padrão?" |
| `re.findall(padrão, texto)` | Lista de strings | Extrair todas as ocorrências |
| `re.finditer(padrão, texto)` | Iterator de match objects | Loop com acesso a grupos |
| `re.sub(padrão, substituição, texto)` | String modificada | Buscar e substituir |
| `re.split(padrão, texto)` | Lista de strings | Separar texto por padrão |
| `re.compile(padrão, flags)` | Objeto regex compilado | Reutilizar padrão |

### Flags

| Flag | Efeito |
|------|--------|
| `re.IGNORECASE` / `re.I` | Ignora maiúsculas/minúsculas |
| `re.MULTILINE` / `re.M` | `^` e `$` passam a funcionar por linha |
| `re.DOTALL` / `re.S` | `.` passa a capturar quebras de linha |

### Métodos do Match Object

| Método | Retorna |
|--------|---------|
| `.group()` | Match inteiro |
| `.group(n)` | Grupo de captura n |
| `.groups()` | Tupla com todos os grupos |
| `.groupdict()` | Dict com grupos nomeados |
| `.start()` | Índice inicial do match |
| `.end()` | Índice final do match |
| `.span()` | Tupla `(start, end)` |

---

## 2. Guia Detalhado

### 1. Metacaracteres Básicos

#### `.` (ponto / dot)

O ponto casa **qualquer caractere exceto quebra de linha**.

```
Padrão: c.t
Texto:  "gato cutuca c4t"
Match:  "gat"  → g a t  (ponto casou com 'a')
        "cut"  → c u t  (ponto casou com 'u')
        "c4t"  → c 4 t  (ponto casou com '4')
```

#### `[...]` (classe de caracteres)

Dentro de colchetes, lista-se os caracteres permitidos. Hífen `-` define intervalo.

```
Padrão: [aeiou]
Texto:  "regex"
Match:  "e", "e"   → todas as vogais

Padrão: [0-9]
Texto:  "Ano 2025"
Match:  "2", "0", "2", "5"   → todos os dígitos
```

#### `[^...]` (classe negada)

O `^` logo após `[` **nega** a classe — casa qualquer caractere **exceto** os listados.

```
Padrão: [^0-9]
Texto:  "A4"
Match:  "A"   → só o que não é dígito
```

---

### 2. Shorthands

| Classe | Shorthand | Match |
|--------|-----------|-------|
| `[0-9]` | `\d` | Qualquer dígito |
| `[^0-9]` | `\D` | Qualquer não-dígito |
| `[a-zA-Z0-9_]` | `\w` | Letra, dígito ou underscore |
| `[^a-zA-Z0-9_]` | `\W` | Tudo que não é `\w` |
| `[ \t\n\r\f\v]` | `\s` | Whitespace (espaço, tab, quebra) |
| `[^ \t\n\r\f\v]` | `\S` | Tudo que não é whitespace |

```python
import re
texto = "ID: A123_XY"
print(re.findall(r'\w+', texto))   # ['ID', 'A123_XY']
print(re.findall(r'\d+', texto))   # ['123']
print(re.findall(r'\D+', texto))   # ['ID: A', '_XY']
```

> 💡 **Dica**: sempre use **raw strings** (`r"..."`) em Python para evitar que `\d` seja interpretado como escape da string.

---

### 3. Quantificadores

Quantificadores definem **quantas vezes** um caractere ou grupo pode aparecer.

```
Texto base: "ac abc abbc abbbc abbbbc"

Padrão ab?c   → "ac"     (b zero ou uma vez)
            → "abc"     (b uma vez)
            → NÃO casa "abbc"

Padrão ab*c   → "ac"     (b zero vezes)
            → "abc"     (b uma vez)
            → "abbc"    (b duas vezes)
            → "abbbc"   (b três vezes)

Padrão ab+c   → "abc"    (b uma vez — "ac" sozinho não casa)
            → "abbc"

Padrão ab{2}c → "abbc"   (exatamente 2 b's)
Padrão ab{2,}c→ "abbc", "abbbc", "abbbbc"  (2 ou mais)
Padrão ab{1,2}c→ "abc", "abbc"            (1 a 2)
```

---

### 4. Âncoras

Âncoras não casam caracteres — casam **posições** na string.

#### `^` — Início

```
Padrão: ^Olá
Texto:  "Olá mundo"
Match:  "Olá"   (no começo)

Texto:  "Diga Olá"
Match:  ❌ (não está no início)
```

#### `$` — Fim

```
Padrão: fim$
Texto:  "Este é o fim"
Match:  "fim"

Texto:  "final feliz"
Match:  ❌
```

#### `\b` — Word boundary (fronteira de palavra)

- `\b` antes: palavra começa naquela posição
- `\b` depois: palavra termina naquela posição

```
Padrão: \bjava\b
Texto:  "java, javascript, javalang"
Match:  "java"   (isolado)
        ❌ dentro de "javascript"
        ❌ dentro de "javalang"
```

---

### 5. Grupos e Backreferences

#### `(...)` — Grupo de captura

Parênteses agrupam parte do padrão **e guardam o valor casado** para uso posterior.

```
Padrão: (\d{2})/(\d{2})/(\d{4})
Texto:  "31/12/2025"
Grupos: \1 = "31"   (dia)
        \2 = "12"   (mês)
        \3 = "2025" (ano)
```

#### `\1` .. `\9` — Backreference

Referencia o que foi capturado por um grupo **anterior** no mesmo padrão.

```
Padrão: (\w)\1      → letra repetida
Texto:  "casa aaah!"
Match:  "aa"        (a seguido de a)
        ❌ "sa"     (s ≠ a)

Padrão: <(\w+)>.*?</\1>   → tag HTML
Texto:  "<b>negrito</b>"
Match:  "<b>negrito</b>"  (\1 = "b" casa com </b>)
```

#### `(?:...)` — Grupo não-capturante

Agrupa sem armazenar — útil para alternação ou quantificação sem poluir os grupos.

```python
import re
texto = "2025-01-01"
# Capturante
m = re.search(r'(\d{4})-(\d{2})-(\d{2})', texto)
print(m.groups())            # ('2025', '01', '01')

# Não-capturante no separador
m = re.search(r'(\d{4})(?:-)(\d{2})(?:-)(\d{2})', texto)
print(m.groups())            # ('2025', '01', '01') — menos grupos!
```

#### `(?P<nome>...)` — Grupo nomeado

Dá um **nome** ao grupo, acessível via `.group('nome')` ou `.groupdict()`.

```python
m = re.search(r'(?P<ano>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2})', "2025-01-01")
print(m.group('ano'))     # '2025'
print(m.groupdict())      # {'ano': '2025', 'mes': '01', 'dia': '01'}
```

---

### 6. Alternação

O `|` funciona como **OU** lógico dentro da regex.

```
Padrão: sim|não|talvez
Texto:  "sim, talvez, não"
Match:  "sim", "talvez", "não"

Padrão: segunda|terça|quarta
Texto:  "Hoje é terça-feira"
Match:  "terça"
```

> ⚠️ A alternação tende a ser **gulosa**: `ab|abc` em "abc" casa `ab`, não `abc`. Para garantir a ordem, coloque a mais longa primeiro: `abc|ab`.

---

### 7. Escape

Para casar um metacharacter **literalmente**, use `\` antes dele.

| Para casar | Escreva |
|------------|---------|
| `.` | `\.` |
| `*` | `\*` |
| `+` | `\+` |
| `?` | `\?` |
| `[` | `\[` |
| `]` | `\]` |
| `(` | `\(` |
| `)` | `\)` |
| `{` | `\{` |
| `}` | `\}` |
| `^` | `\^` |
| `$` | `\$` |
| `\|` | `\|` |
| `\` | `\\\\` (sim, quatro!) |

```
Padrão: \d+\.\d+
Texto:  "Preço: 29.90"
Match:  "29.90"   (ponto literal)
```

Em Python raw strings, `\.` é suficiente. Sem raw string, você precisaria escrever `\\.`.

---

### 8. Wildcard `.*`

`.*` = `.` (qualquer char) + `*` (zero ou mais) → casa **qualquer coisa** entre dois pontos.

```
Padrão: <.*>
Texto:  "<b>texto</b>"
Match:  "<b>texto</b>"   → GULOSO: foi do primeiro < até o último >
```

> Veja abaixo como `.*?` (lazy) muda o comportamento.

---

### 9. Greedy vs Lazy

Por padrão, quantificadores são **gulosos (greedy)** — casam o **máximo possível**.

O `?` após um quantificador o torna **lazy** — casa o **mínimo necessário**.

```
Texto: "<b>negrito</b> e <i>itálico</i>"

Greedy: <.*>   → "<b>negrito</b> e <i>itálico</i>"
                  (um único match gigante, do 1º < ao último >)

Lazy:   <.*?>  → "<b>", "</b>", "<i>", "</i>"
                  (quatro matches, cada tag separada)
```

| Guloso | Lazy | Casa |
|--------|------|------|
| `*` | `*?` | mínimo possível |
| `+` | `+?` | mínimo possível (pelo menos 1) |
| `?` | `??` | mínimo possível (0 ou 1) |
| `{n,m}` | `{n,m}?` | mínimo possível |

---

### 10. Funções `re.xxx`

#### `re.search()` — Primeira ocorrência

Retorna um **match object** ou `None`.

```python
import re

texto = "Meu email é joao@email.com e o suporte@empresa.com"
m = re.search(r'\w+@\w+\.\w+', texto)

if m:
    print(m.group())          # 'joao@email.com'  (só o primeiro!)
```

#### `re.findall()` — Todas as ocorrências

Retorna uma **lista de strings** (ou lista de tuplas se houver grupos).

```python
texto = "joao@email.com, suporte@empresa.com"
emails = re.findall(r'\w+@\w+\.\w+', texto)
print(emails)                 # ['joao@email.com', 'suporte@empresa.com']

# Com grupos — retorna tuplas
pares = re.findall(r'(\w+)@(\w+)\.\w+', texto)
print(pares)                  # [('joao', 'email'), ('suporte', 'empresa')]
```

#### `re.finditer()` — Iterator de match objects

Igual `findall`, mas retorna um **iterador** de match objects — útil para acessar `.group()`, `.span()`, etc.

```python
texto = "joao@email.com, suporte@empresa.com"
for m in re.finditer(r'(\w+)@(\w+)\.\w+', texto):
    print(f"Usuário: {m.group(1)}, Domínio: {m.group(2)}")
    print(f"Posição: {m.span()}")
# Usuário: joao, Domínio: email
# Posição: (0, 15)
# Usuário: suporte, Domínio: empresa
# Posição: (17, 37)
```

#### `re.sub()` — Substituir

```python
texto = "Hoje é 31/12/2025"
# Substituir data DD/MM/AAAA por AAAA-MM-DD
novo = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\3-\2-\1', texto)
print(novo)                # 'Hoje é 2025-12-31'

# Substituir com função
def mascarar(m):
    return '*' * len(m.group())

texto = "Cartão: 1234 5678 9012 3456"
print(re.sub(r'\d{4} \d{4} \d{4} \d{4}', mascarar, texto))
# 'Cartão: *******************'
```

#### `re.split()` — Dividir por padrão

```python
texto = "um, dois; três|quatro"
partes = re.split(r'[,;|]', texto)
print(partes)              # ['um', ' dois', ' três', 'quatro']
```

#### `re.compile()` — Compilar para reuso

Compila um padrão uma vez e reutiliza — **mais performático** em loops.

```python
# Sem compile
for linha in arquivo:
    if re.search(r'\d{4}-\d{2}-\d{2}', linha):
        ...

# Com compile
padrao_data = re.compile(r'\d{4}-\d{2}-\d{2}')
for linha in arquivo:
    if padrao_data.search(linha):
        ...
```

---

### 11. Flags

Flags modificam o comportamento da regex. Passam como 3º argumento (ou dentro de `compile()`).

#### `re.IGNORECASE` (ou `re.I`)

```python
re.search(r'python', 'Python é legal', re.I)
# Match independente de maiúscula/minúscula
```

#### `re.MULTILINE` (ou `re.M`)

Faz `^` e `$` casarem **início/fim de cada linha**, não só da string inteira.

```python
texto = """linha 1
linha 2
linha 3"""

# Sem MULTILINE: ^ casa só antes de "linha 1"
print(re.findall(r'^\w+', texto))          # ['linha']

# Com MULTILINE: ^ casa início de cada linha
print(re.findall(r'^\w+', texto, re.M))    # ['linha', 'linha', 'linha']
```

#### `re.DOTALL` (ou `re.S`)

Faz o `.` casar **inclusive quebra de linha**.

```python
texto = "<b>negrito\ncontinua</b>"

# Sem DOTALL: . não casa \n
print(re.findall(r'<b>.*</b>', texto))     # []

# Com DOTALL: . casa \n também
print(re.findall(r'<b>.*</b>', texto, re.S))
# ['<b>negrito\ncontinua</b>']
```

---

### 12. Match Object

Quando `re.search()` ou `re.finditer()` encontram um match, retornam um **match object** com métodos úteis.

```python
texto = "Data: 31/12/2025"
m = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)

print(m.group())       # '31/12/2025'    (match completo)
print(m.group(1))      # '31'            (1º grupo)
print(m.group(2))      # '12'            (2º grupo)
print(m.group(3))      # '2025'          (3º grupo)
print(m.groups())      # ('31', '12', '2025')  (tupla)
print(m.start())       # 6               (índice inicial)
print(m.end())         # 16              (índice final)
print(m.span())        # (6, 16)         (tupla start/end)
```

---

### 13. Named Groups com `groupdict()`

Grupos nomeados com `(?P<nome>...)` tornam o código mais legível.

```python
padrao = r'(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<ano>\d{4})'
texto  = "31/12/2025"

m = re.search(padrao, texto)
print(m.group('dia'))      # '31'
print(m.group('mes'))      # '12'
print(m.group('ano'))      # '2025'
print(m.groupdict())       # {'dia': '31', 'mes': '12', 'ano': '2025'}

# Uso prático: converter para dict e manipular
dados = m.groupdict()
print(f"{dados['ano']}-{dados['mes']}-{dados['dia']}")  # 2025-12-31
```

---

## 3. Exercícios

| Exercício | Resolução |
|-----------|-----------|
| 📝 Lista 1 — Exercícios de Fixação (Regex teórico) | Arquivo original: [`03 - Lista 1 - Exercicios De Fixacao - Regex.odt`](../03%20-%20Regex/03%20-%20Lista%201%20-%20Exercicios%20De%20Fixacao%20-%20Regex.odt) |
| 🐍 Lista 2 — Regex com Python | [📄 Resolução comentada](resolucoes/04%20-%20resolucao%20-%20regex%20com%20python.md) |
| 🏆 Desafio Regex | [📄 Resolução comentada](resolucoes/05%20-%20resolucao%20-%20desafio%20regex.md) |

---

> 📁 **Arquivos originais da disciplina**:
> - [`03 - Regex/01 - Slides - Expressoes Regulares.pptx`](../03%20-%20Regex/01%20-%20Slides%20-%20Expressoes%20Regulares.pptx)
> - [`03 - Regex/02 - Slides - Outros Metacaracteres.pptx`](../03%20-%20Regex/02%20-%20Slides%20-%20Outros%20Metacaracteres.pptx)
> - [`04 - Regex Com Python/01 - Slides - Regex Com Python.odp`](../04%20-%20Regex%20Com%20Python/01%20-%20Slides%20-%20Regex%20Com%20Python.odp)
> - [`04 - Regex Com Python/02 - Lista 2 - Regex Com Python.odt`](../04%20-%20Regex%20Com%20Python/02%20-%20Lista%202%20-%20Regex%20Com%20Python.odt)
> - [`04 - Regex Com Python/03 - Desafio - Expressoes Regulares Com Python.odt`](../04%20-%20Regex%20Com%20Python/03%20-%20Desafio%20-%20Expressoes%20Regulares%20Com%20Python.odt)
>
> 📚 **Materiais de apoio**:
> - [`00 - Materiais De Apoio/02 - Apostila Expressoes Regulares - Aurelio Marinho Jargas.pdf`](../00%20-%20Materiais%20De%20Apoio/02%20-%20Apostila%20Expressoes%20Regulares%20-%20Aurelio%20Marinho%20Jargas.pdf)
