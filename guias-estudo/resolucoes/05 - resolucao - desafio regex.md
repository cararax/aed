# Resolução — Desafio Regex: Validação de Cadastro de Produtos

> **Baseado no dataset:** `04 - Regex Dataset.txt` (12 produtos, alguns intencionalmente inválidos)
> **Código de referência:** `05 - Avaliacao - Regex Com Python.py`

## Solução completa

```python
import re

# =====================================================================
# DATASET: produtos extraídos de "04 - Regex Dataset.txt"
# Cada entrada é um dicionário com: nome, codigo, preco, validade
# =====================================================================
dados_produtos = [
    # Totalmente válidos
    {"nome": "Camiseta Polo Masculina",      "codigo": "ABCDEF1234", "preco": "99.99",   "validade": "15/12/2025"},
    {"nome": "Tênis Esportivo Masculino",     "codigo": "ZXCVBN5678", "preco": "149,90",  "validade": "01/01/2026"},
    {"nome": "Bermuda Jeans Masculina",       "codigo": "QWERTY0001", "preco": "79.9",    "validade": "31/10/2025"},
    {"nome": "Vestido Longo Estampado",       "codigo": "LONGDR1234", "preco": "120.00",  "validade": "28/02/2024"},

    # Inválidos
    {"nome": "camiseta polo masculina",       "codigo": "abcdef1234", "preco": "99.999",  "validade": "15/12/25"},
    {"nome": "Camisa Masculina",              "codigo": "ABC1234@",   "preco": "-49,90",  "validade": "32/12/2025"},
    {"nome": "Calça Jeans Slim",              "codigo": "ABCDE1234",  "preco": "100,999", "validade": "30-12-2025"},
    {"nome": "Blusa De Frio",                 "codigo": "1234567890", "preco": "0.00",    "validade": "00/00/0000"},
    {"nome": "Jaqueta Masculina Couro",       "codigo": "C0D1C01234", "preco": "abc",     "validade": "31/04/2025"},
    {"nome": "Boné Vermelho Casual",          "codigo": "VERMEL0000", "preco": "199",     "validade": "29/02/2023"},
    {"nome": "Mochila Escolar Grande",        "codigo": "MOCHIL123",  "preco": "250.5",   "validade": "12/13/2025"},
    {"nome": "Tênis Corrida Branco",          "codigo": "RUNSHO1234", "preco": "300,00",  "validade": "15/06/2030"},
]

# =====================================================================
# 1. REGRA — NOME DO PRODUTO
#    - Palavras iniciando com letra maiúscula
#    - Mínimo 3 palavras
#    - Separadas por espaços
# =====================================================================
# Padrão: 3 ocorrências de: borda de palavra, letra maiúscula + \w+, espaço opcional
# \b       → borda de palavra (garante início da palavra)
# [A-Z]    → primeira letra maiúscula (sem acentos no dataset)
# \w+      → restante da palavra (letras, números, underscore)
# \s?      → espaço opcional entre palavras
# {3}      → quantificador: exige exatamente 3 palavras (no mínimo)
# (?P<palavra>...) → grupo nomeado para cada palavra
pattern_nome = re.compile(r'(?P<palavra>\b[A-Z]\w+\s?){3}')

# fullmatch() exige que a string INTEIRA se encaixe no padrão
# → "Camisa Masculina" (2 palavras) falha, "camiseta polo..." (minúscula) falha

# =====================================================================
# 2. REGRA — CÓDIGO DO PRODUTO
#    - 6 letras maiúsculas + 4 dígitos
#    - Sem espaços ou caracteres especiais
# =====================================================================
# [A-Z]{6}  → exatamente 6 letras maiúsculas
# \d{4}     → exatamente 4 dígitos
# ^...$     → âncoras (implícitas no fullmatch)
pattern_codigo = re.compile(r'(?P<codigo>[A-Z]{6}\d{4})')

# "abcdef1234" → falha (minúsculas)
# "ABC1234@"   → falha (caractere especial)
# "ABCDE1234"  → falha (5 letras em vez de 6)
# "C0D1C01234" → falha (dígito no meio das letras)
# "MOCHIL123"  → falha (3 dígitos em vez de 4)

# =====================================================================
# 3. REGRA — PREÇO
#    - Número positivo com até 2 casas decimais
#    - Separador pode ser ponto (.) ou vírgula (,)
#    - Parte inteira obrigatória (1 ou mais dígitos)
# =====================================================================
# ^\d+       → um ou mais dígitos no início (parte inteira)
# [.,]       → separador decimal (ponto ou vírgula)
# \d{1,2}$   → de 1 a 2 dígitos decimais no final
#
# Observação: este padrão NÃO aceita inteiros sem casa decimal (ex.: "199").
# O padrão do autor original cobre esse caso separadamente, mas aqui
# seguimos a especificação à risca: "com até 2 casas decimais" implica
# que a casa decimal é esperada. Para aceitar também inteiros, bastaria
# tornar a parte decimal opcional com (?:[.,]\d{1,2})?$ .
pattern_preco = re.compile(
    r'(?P<inteiro>^\d+)'        # parte inteira (1+ dígitos)
    r'(?P<separador>[.,])'      # separador: ponto ou vírgula
    r'(?P<decimais>\d{1,2})$'   # até 2 casas decimais
)

# "99.999" → falha (3 casas decimais)
# "-49,90" → falha (sinal negativo)
# "abc"    → falha (não é número)
# "250.5"  → OK (1 casa decimal, dentro do limite)

# =====================================================================
# 4. REGRA — DATA DE VALIDADE
#    - Formato DD/MM/AAAA
#    - Dia: 01–31, Mês: 01–12, Ano: exatamente 4 dígitos
# =====================================================================
# Dia: 01-09 | 10-19 | 20-29 | 30-31
#   0[1-9]  → 01 a 09
#   1\d     → 10 a 19
#   2\d     → 20 a 29
#   3[0-1]  → 30 ou 31
# Mês: 01-09 | 10-12
#   0[1-9]  → 01 a 09
#   1[0-2]  → 10, 11, 12
# Ano: \d{4} → exatamente 4 dígitos
pattern_data = re.compile(
    r'(?P<dia>0[1-9]|1\d|2\d|3[0-1])'   # dia entre 01 e 31
    r'/'                                  # separador barra
    r'(?P<mes>0[1-9]|1[0-2])'           # mês entre 01 e 12
    r'/'                                  # separador barra
    r'(?P<ano>\d{4})'                    # ano com 4 dígitos
)

# "15/12/25"   → falha (ano com 2 dígitos)
# "32/12/2025" → falha (dia 32)
# "30-12-2025" → falha (separador errado)
# "00/00/0000" → falha (00 não é dia/mês válido)
# Nota: validação lógica (ex.: 31/04, 29/02/2023 não bissexto) requer
#        processamento adicional além da regex.

# =====================================================================
# VALIDAÇÃO — aplica todos os padrões contra o dataset
# =====================================================================
print(f'{"NOME":35s} {"CÓDIGO":15s} {"PREÇO":10s} {"VALIDADE":12s} {"STATUS"}')
print('-' * 90)

for produto in dados_produtos:
    nome_ok     = bool(pattern_nome.fullmatch(produto["nome"]))
    codigo_ok   = bool(pattern_codigo.fullmatch(produto["codigo"]))
    preco_ok    = bool(pattern_preco.fullmatch(produto["preco"]))
    data_ok     = bool(pattern_data.fullmatch(produto["validade"]))

    # Se todos os 4 campos forem válidos → "VÁLIDO", senão → "INVÁLIDO"
    status = "VÁLIDO" if (nome_ok and codigo_ok and preco_ok and data_ok) else "INVÁLIDO"

    print(f'{produto["nome"]:35s} {produto["codigo"]:15s} '
          f'{produto["preco"]:10s} {produto["validade"]:12s} [{status}]')
```

## Saída esperada

```
NOME                               CÓDIGO           PREÇO      VALIDADE       STATUS
------------------------------------------------------------------------------------------
Camiseta Polo Masculina            ABCDEF1234       99.99      15/12/2025     [VÁLIDO]
Tênis Esportivo Masculino          ZXCVBN5678       149,90     01/01/2026     [VÁLIDO]
Bermuda Jeans Masculina            QWERTY0001       79.9       31/10/2025     [VÁLIDO]
Vestido Longo Estampado            LONGDR1234       120.00     28/02/2024     [VÁLIDO]
camiseta polo masculina            abcdef1234       99.999     15/12/25       [INVÁLIDO]
Camisa Masculina                   ABC1234@         -49,90     32/12/2025     [INVÁLIDO]
Calça Jeans Slim                   ABCDE1234        100,999    30-12-2025     [INVÁLIDO]
Blusa De Frio                      1234567890       0.00       00/00/0000     [INVÁLIDO]
Jaqueta Masculina Couro            C0D1C01234       abc        31/04/2025     [INVÁLIDO]
Boné Vermelho Casual               VERMEL0000       199        29/02/2023     [INVÁLIDO]
Mochila Escolar Grande             MOCHIL123        250.5      12/13/2025     [INVÁLIDO]
Tênis Corrida Branco               RUNSHO1234       300,00     15/06/2030     [VÁLIDO]
```

## Observações sobre validação lógica

A regex valida o **formato**, mas não consegue validar a **semântica** completa:

| Situação | Regex captura? | Logicamente válido? |
|---|---|---|
| `31/04/2025` | ✓ dia 31, mês 04 | ✗ abril tem 30 dias |
| `29/02/2023` | ✓ dia 29, mês 02 | ✗ 2023 não é bissexto |
| `29/02/2024` | ✓ dia 29, mês 02 | ✓ 2024 é bissexto |

Para validação lógica completa, seria necessário um passo extra usando
o módulo `datetime`:

```python
from datetime import datetime

def validar_data_logica(data_str: str) -> bool:
    """Valida se a data realmente existe no calendário."""
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False
```
