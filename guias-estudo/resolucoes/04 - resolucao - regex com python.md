# Resolução — Regex com Python

## Exercício 1 — Server Log Analyzer

```python
import re

# --- Padrão regex compilado com grupos nomeados ---
# Explicação do padrão:
# (?P<ip>\d+\.\d+\.\d+\.\d+)  → captura o IP (4 octetos separados por ponto) no grupo "ip"
# \[(?P<data>[^\]]+)\]         → captura o conteúdo dentro de colchetes como a data/hora
# "GET|POST                     → método HTTP literal (GET ou POST)
# (?P<path>\S+)                 → captura o caminho/path (qualquer caractere não-espaço)
# HTTP/\d+\.\d+"                → versão do protocolo HTTP
# (?P<status>\d{3})             → captura o código de status (3 dígitos)
pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)'       # IP do cliente
    r' - \['                             # literal " - ["
    r'(?P<data>[^\]]+)'                  # data/hora (tudo até o ']')
    r'\] "'                               # fechamento do colchete + aspas
    r'(?:GET|POST) '                      # método HTTP (não-capturante)
    r'(?P<path>\S+)'                      # caminho requisitado
    r' HTTP/\d+\.\d+" '                  # protocolo HTTP
    r'(?P<status>\d{3})'                  # código de status
)

# Dados de teste (3 linhas de log)
logs = [
    '192.168.0.15 - [24/Mar/2026:10:20:01] "GET /index.html HTTP/1.1" 200',
    '10.0.0.5 - [24/Mar/2026:11:45:33] "POST /api/login HTTP/1.1" 401',
    '172.16.0.100 - [24/Mar/2026:14:02:17] "GET /produtos?id=42 HTTP/1.1" 200',
]

# Processamento de cada linha usando .groupdict()
for linha in logs:
    match = pattern.match(linha)
    if match:
        dados = match.groupdict()  # → {"ip": "...", "data": "...", "path": "...", "status": "..."}
        print(f'O IP {dados["ip"]} tentou acessar {dados["path"]} e recebeu status {dados["status"]}.')
    else:
        print(f'Linha não reconhecida: {linha}')
```

**Saída esperada:**

```
O IP 192.168.0.15 tentou acessar /index.html e recebeu status 200.
O IP 10.0.0.5 tentou acessar /api/login e recebeu status 401.
O IP 172.16.0.100 tentou acessar /produtos?id=42 e recebeu status 200.
```

---

## Exercício 2 — Product Catalog Standardizer

```python
import re

# --- Padrão regex para extrair Produto, Quantidade e SKU ---
# Explicação do padrão:
# (?P<produto>.+?)          → grupo nomeado "produto": um ou mais caracteres (lazy), até o " -"
# Quantidade:\s*(\d+)       → captura o número após "Quantidade:" (grupo numerado \1)
# SKU:\s*(\w+)              → captura o código alfanumérico após "SKU:" (grupo numerado \2)
pattern = re.compile(
    r'(?P<produto>.+?)'          # nome do produto (captura mínima até o " -")
    r' - Quantidade: (\d+)'     # grupo \1 → quantidade
    r' - SKU: (\w+)'            # grupo \2 → código SKU
)

# Dados de teste
entradas = [
    "Parafuso Sextavado - Quantidade: 500 - SKU: PAR123",
    "Martelo de Unha - Quantidade: 12 - SKU: MAR001",
    "Tinta Acrílica Branca - Quantidade: 5 - SKU: TIN99",
]

# Transformação usando re.sub() com grupos numerados (\1, \2)
# Template de saída: "SKU_<SKU>: <Produto> (<Quantidade> unidades)"
# \2 → SKU,  \1 → Quantidade,  (?P=produto) → nome do produto
# Obs.: como usamos named group para produto, acessamos pelo nome na função de re.sub.
def transformar(entrada: str) -> str:
    """Converte 'Produto - Qtd: N - SKU: C' → 'SKU_C: Produto (N unidades)'"""
    match = pattern.match(entrada)
    if match:
        produto  = match.group('produto')
        qtd      = match.group(1)
        sku      = match.group(2)
        return f'SKU_{sku}: {produto} ({qtd} unidades)'
    return entrada  # fallback: retorna original se não casar

# Aplicando a transformação
for entrada in entradas:
    print(transformar(entrada))
```

**Saída esperada:**

```
SKU_PAR123: Parafuso Sextavado (500 unidades)
SKU_MAR001: Martelo de Unha (12 unidades)
SKU_TIN99: Tinta Acrílica Branca (5 unidades)
```
