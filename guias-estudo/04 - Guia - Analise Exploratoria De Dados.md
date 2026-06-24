# Análise Exploratória de Dados (AED) com Pandas

> Baseado nos notebooks da pasta [`07 - Analise De Dados/`](../07%20-%20Analise%20De%20Dados/)

---

## Sumário

- [Quick Reference](#quick-reference)
- [Guia Detalhado](#guia-detalhado)
  - [1. Carregar e Inspecionar Dados](#1-carregar-e-inspecionar-dados)
  - [2. Limpeza Básica](#2-limpeza-básica)
  - [3. Filtros e Seleções](#3-filtros-e-seleções)
  - [4. Novas Colunas](#4-novas-colunas)
  - [5. Agrupamento e Agregação](#5-agrupamento-e-agregação)
  - [6. Visualização com Seaborn + Matplotlib](#6-visualização-com-seaborn--matplotlib)
  - [7. Análise Multivariada com hue](#7-análise-multivariada-com-hue)
- [Exercícios Resolvidos](#exercícios-resolvidos)

---

## Quick Reference

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv("arquivo.csv")

# Inspecionar
df.head()          # primeiras 5 linhas
df.info()          # tipos, nulos, memória
df.describe()      # estatísticas descritivas

# Frequências
df['coluna'].value_counts()
df['coluna'].value_counts(normalize=True)  # percentuais

# Filtro booleano
df[df['preco'] > 50]
df[(df['categoria'] == 'Tecnologia') & (df['preco'] < 100)]

# Top N valores
df.nlargest(5, 'preco')
df.nsmallest(3, 'quantidade_vendida')

# Nova coluna
df['faturamento'] = df['preco'] * df['quantidade_vendida']

# Agrupar e agregar
df.groupby('categoria')['preco'].mean()
df.groupby('categoria').agg({'preco': 'mean', 'quantidade_vendida': 'sum'})

# Gráficos Seaborn
sns.countplot(data=df, x='categoria')
sns.histplot(data=df, x='preco', bins=20)
sns.scatterplot(data=df, x='preco', y='avaliacao_media')
sns.barplot(data=df, x='categoria', y='faturamento')

# Personalização
plt.title("Título")
plt.xlabel("Eixo X")
plt.ylabel("Eixo Y")
plt.show()
```

---

## Guia Detalhado

### 1. Carregar e Inspecionar Dados

```python
import pandas as pd

df = pd.read_csv("04 - Dados - Gorjetas.csv")
```

| Método | O que mostra |
|--------|-------------|
| `df.head(n)` | Primeiras `n` linhas (padrão 5) |
| `df.info()` | Colunas, tipos (`int64`, `float64`, `object`), contagem de não-nulos |
| `df.describe()` | Média, desvio padrão, min, max, quartis (só colunas numéricas) |
| `df.shape` | Tupla `(linhas, colunas)` |
| `df.columns` | Lista de nomes das colunas |
| `df.dtypes` | Tipo de cada coluna |
| `df.isnull().sum()` | Contagem de valores ausentes por coluna |

**Exemplo com `tips.csv` (gorjetas):**

```python
df = pd.read_csv("04 - Dados - Gorjetas.csv")
df.head()
```

| total_bill | tip | sex | smoker | day | time | size |
|------------|-----|-----|--------|-----|------|------|
| 16.99 | 1.01 | Female | No | Sun | Dinner | 2 |
| 10.34 | 1.66 | Male | No | Sun | Dinner | 3 |

```python
df.info()
# RangeIndex: 244 entries
# Data columns: total_bill(float64), tip(float64), sex(object), smoker(object), day(object), time(object), size(int64)

df.describe()
#        total_bill        tip        size
# mean    19.78        2.998       2.569
# std      8.902       1.383       0.951
# min      3.07        1.00        1
# max      50.81       10.00       6
```

> Arquivo original: [`04 - Dados - Gorjetas.csv`](../07%20-%20Analise%20De%20Dados/04%20-%20Dados%20-%20Gorjetas.csv)

#### value_counts() — Frequências

```python
df['day'].value_counts()
# Sat    87
# Sun    76
# Thur   62
# Fri    19

df['sex'].value_counts(normalize=True)  # proporção (0~1)
# Male      0.643
# Female    0.357
```

---

### 2. Limpeza Básica

Antes de analisar, é essencial verificar a **qualidade dos dados**.

**Verificar valores ausentes:**

```python
df.isnull().sum()
```

**Remover ou preencher nulos:**

```python
df.dropna()                    # remove linhas com qualquer NaN
df.dropna(subset=['coluna'])   # remove só se NaN na coluna específica
df['coluna'].fillna(valor)     # preenche NaN com um valor
```

**Detectar outliers (exemplo com `Ecommerce.csv`):**

```python
df = pd.read_csv("02 - Dados - Ecommerce.csv")
df.describe()
# idade: min=-10, max=300 → valores inválidos!
# tempo_sessao_minutos: min=0.0, max=1440 → outlier (24h)

# Filtrar idades válidas (ex: 0-100)
df = df[(df['idade'] >= 0) & (df['idade'] <= 100)]

# Filtrar tempo de sessão razoável (ex: < 120 min)
df = df[df['tempo_sessao_minutos'] < 120]
```

> Arquivo original: [`02 - Dados - Ecommerce.csv`](../07%20-%20Analise%20De%20Dados/02%20-%20Dados%20-%20Ecommerce.csv)

**Verificar valores únicos em colunas categóricas:**

```python
df['origem_trafego'].value_counts()
# Mobile     ...
# Desktop    ...
# Tablet     ...
```

---

### 3. Filtros e Seleções

**Filtro booleano simples:**

```python
# Clientes que pagaram conta > 20
caros = df[df['total_bill'] > 20]

# Apenas mulheres
mulheres = df[df['sex'] == 'Female']
```

**Múltiplas condições (use `&` para "e", `|` para "ou"):**

```python
# Homens não-fumantes com conta > 30
filtro = df[(df['sex'] == 'Male') & (df['smoker'] == 'No') & (df['total_bill'] > 30)]
```

> ⚠️ Cada condição precisa de parênteses! `df['sex'] == 'Male' & df['smoker'] == 'No'` → erro.

**Selecionar colunas específicas:**

```python
df[['total_bill', 'tip', 'day']]
```

**nlargest() / nsmallest() — Top N:**

```python
# 5 maiores contas
df.nlargest(5, 'total_bill')

# 3 menores gorjetas
df.nsmallest(3, 'tip')

# Com várias colunas (desempate)
df.nlargest(5, ['total_bill', 'tip'])
```

---

### 4. Novas Colunas

Criar colunas derivadas de operações entre colunas existentes:

```python
# Proporção da gorjeta em relação à conta
df['tip_percent'] = df['tip'] / df['total_bill'] * 100

# Faturamento (livraria)
df['faturamento'] = df['preco'] * df['quantidade_vendida']
```

**Exemplo completo com `livraria.csv`:**

```python
df = pd.read_csv("06 - Dados - Livraria.csv")
df['faturamento'] = df['preco'] * df['quantidade_vendida']
df.head()
```

| titulo | categoria | preco | quantidade_vendida | faturamento |
|--------|-----------|-------|-------------------|-------------|
| Python para Iniciantes | Tecnologia | 79.9 | 120 | 9588.0 |
| História do Brasil | História | 54.5 | 85 | 4632.5 |

> Arquivo original: [`06 - Dados - Livraria.csv`](../07%20-%20Analise%20De%20Dados/06%20-%20Dados%20-%20Livraria.csv)

---

### 5. Agrupamento e Agregação

**Agrupar por uma categoria e calcular estatísticas:**

```python
# Gorjeta média por dia
df.groupby('day')['tip'].mean()

# day
# Fri    2.734737
# Sat    2.993103
# Sun    3.255132
# Thur   2.771452

# Contagem de clientes por dia
df.groupby('day').size()
# ou
df['day'].value_counts()
```

**Múltiplas agregações com `.agg()`:**

```python
df.groupby('day').agg({
    'total_bill': 'mean',
    'tip': ['mean', 'sum', 'count'],
    'size': 'max'
})
```

**Agrupar por duas colunas:**

```python
df.groupby(['day', 'time'])['tip'].mean()
```

**Exemplo — faturamento por categoria (livraria):**

```python
df.groupby('categoria')['faturamento'].sum().sort_values(ascending=False)
```

---

### 6. Visualização com Seaborn + Matplotlib

**countplot — contagem de categorias:**

```python
sns.countplot(data=df, x='day')
plt.title("Número de Clientes por Dia")
plt.show()
```

**histplot — distribuição de uma variável numérica:**

```python
sns.histplot(data=df, x='total_bill', bins=20)
plt.title("Distribuição do Valor da Conta")
plt.xlabel("Total da Conta (R$)")
plt.ylabel("Frequência")
plt.show()
```

**scatterplot — relação entre duas variáveis:**

```python
sns.scatterplot(data=df, x='total_bill', y='tip')
plt.title("Relação Conta vs Gorjeta")
plt.show()
```

**barplot — média de uma variável por categoria:**

```python
sns.barplot(data=df, x='day', y='tip')
plt.title("Gorjeta Média por Dia")
plt.show()
```

---

### 7. Análise Multivariada com hue

O parâmetro `hue` adiciona uma **terceira dimensão** (cor) ao gráfico:

```python
# Gorjeta média por dia, separando por sexo
sns.barplot(data=df, x='day', y='tip', hue='sex')
plt.title("Gorjeta Média por Dia e Sexo")
plt.show()

# Dispersão conta vs gorjeta, colorindo por fumante/não-fumante
sns.scatterplot(data=df, x='total_bill', y='tip', hue='smoker')
plt.title("Relação Conta vs Gorjeta (por Fumante)")
plt.show()

# Contagem de clientes por dia, separando por período (almoço/jantar)
sns.countplot(data=df, x='day', hue='time')
plt.title("Clientes por Dia e Período")
plt.show()
```

**Dica:** use `hue` sempre que quiser comparar subgrupos dentro de uma mesma visualização.

---

## Exercícios Resolvidos

| Exercício | Resolução |
|-----------|-----------|
| 📚 Livraria — Análise de Dados | [📄 Resolução comentada](resolucoes/08%20-%20resolucao%20-%20livraria%20aed.md) |
| 🛒 Trabalho 2 — AED (E-commerce + Feedback) | [📄 Resolução comentada](resolucoes/09%20-%20resolucao%20-%20trabalho%202%20aed.md) |

---

> 📎 **Arquivos originais da disciplina**: pasta [`07 - Analise De Dados/`](../07%20-%20Analise%20De%20Dados/)
> 📁 Slides: [`01 - Slides - Analise Exploratoria De Dados.pptx`](../07%20-%20Analise%20De%20Dados/01%20-%20Slides%20-%20Analise%20Exploratoria%20De%20Dados.pptx)
