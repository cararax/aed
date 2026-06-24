# Resolução — Análise Exploratória de Dados: Livraria

## 1. Importação dos dados

```python
# Importa a biblioteca pandas para manipulação dos dados
import pandas as pd

# Carrega o dataset "livraria.csv" para um DataFrame chamado df
df = pd.read_csv("livraria.csv")

# Exibe as 5 primeiras linhas para inspecionar o conteúdo
df.head()
"""
Saída esperada (exemplo):
                     titulo       categoria  preco  quantidade_vendida  avaliacao_media  estoque
0        O Senhor dos Anéis        Fantasia  49.90                 120              4.8       35
1      Cem Anos de Solidão         Romance   39.90                  85              4.7       20
2            1984                Ficção Científica  34.90                 200              4.9       50
3  O Pequeno Príncipe           Infantil    29.90                 300              4.9       15
4          Dom Casmurro           Romance   19.90                 150              4.5       40
"""
```

## 2. Visão geral do dataset

```python
# Verifica o número de linhas e colunas
print("Shape (linhas, colunas):", df.shape)
# Saída: (N, 6) onde N é o número total de livros

# Lista os tipos de dados de cada coluna
print("\nTipos de dados:\n", df.dtypes)

# Verifica se há valores ausentes em cada coluna
print("\nValores ausentes por coluna:\n", df.isna().sum())
```

**Análise:** O .shape informa quantas linhas (livros) e colunas (atributos) existem. Os .dtypes mostram que `preco`, `quantidade_vendida`, `avaliacao_media` e `estoque` são numéricos, enquanto `titulo` e `categoria` são texto. O `isna().sum()` revela se há dados faltantes — se houver, será necessário tratá-los.

## 3. Estatísticas descritivas

```python
# Gera o resumo estatístico das colunas numéricas
desc = df.describe()
print(desc)

# Extrai o preço médio dos livros
preco_medio = df['preco'].mean()
print(f"Preço médio dos livros: R$ {preco_medio:.2f}")

# Extrai a avaliação média geral
avaliacao_media = df['avaliacao_media'].mean()
print(f"Avaliação média geral: {avaliacao_media:.2f} estrelas")
```

**Análise:** O `describe()` fornece média, desvio padrão, mínimo, máximo e quartis. A média de `preco` revela o ticket médio da livraria, e a média de `avaliacao_media` mostra a satisfação geral dos leitores.

## 4. Análise por categoria

```python
# Lista as categorias únicas de livros
categorias_unicas = df['categoria'].unique()
print("Categorias únicas:", categorias_unicas)

# Calcula a quantidade total vendida por categoria
qtd_por_categoria = df.groupby('categoria')['quantidade_vendida'].sum()
print("\nQuantidade total vendida por categoria:\n", qtd_por_categoria)

# Calcula o faturamento total por categoria (preço * quantidade)
df['faturamento_temp'] = df['preco'] * df['quantidade_vendida']
faturamento_por_categoria = df.groupby('categoria')['faturamento_temp'].sum()
categoria_maior_faturamento = faturamento_por_categoria.idxmax()
print(f"\nCategoria com maior faturamento: {categoria_maior_faturamento}")
print(f"Faturamento: R$ {faturamento_por_categoria.max():.2f}")

# Remove a coluna temporária (será recriada no passo 5)
df.drop(columns='faturamento_temp', inplace=True)

# Calcula a média de avaliação por categoria
avaliacao_por_categoria = df.groupby('categoria')['avaliacao_media'].mean()
melhor_categoria_avaliacao = avaliacao_por_categoria.idxmax()
print(f"\nCategoria com melhor avaliação média: {melhor_categoria_avaliacao}")
print(f"Média: {avaliacao_por_categoria.max():.2f}")
```

**Análise:** O `groupby()` agrega os dados por categoria. A soma de `quantidade_vendida` mostra quais categorias vendem mais unidades. O faturamento (preço × quantidade) identifica a categoria que mais gera receita. A média de `avaliacao_media` revela a categoria mais bem avaliada pelos clientes.

## 5. Exploração adicional

```python
# Cria a coluna de faturamento (preço * quantidade vendida)
df['faturamento'] = df['preco'] * df['quantidade_vendida']

# Encontra o livro mais caro e o mais barato
livro_mais_caro = df.loc[df['preco'].idxmax()]
livro_mais_barato = df.loc[df['preco'].idxmin()]
print("Livro mais caro:")
print(livro_mais_caro[['titulo', 'preco']])
print("\nLivro mais barato:")
print(livro_mais_barato[['titulo', 'preco']])

# Exibe os 3 livros mais vendidos (maior quantidade_vendida)
top3_vendas = df.nlargest(3, 'quantidade_vendida')[['titulo', 'quantidade_vendida']]
print("\nTop 3 livros mais vendidos:\n", top3_vendas)

# Gráfico de barras com o faturamento por categoria
import matplotlib.pyplot as plt

faturamento_cat = df.groupby('categoria')['faturamento'].sum().sort_values()
faturamento_cat.plot(kind='barh', figsize=(10, 6), color='steelblue')
plt.title('Faturamento Total por Categoria')
plt.xlabel('Faturamento (R$)')
plt.ylabel('Categoria')
plt.tight_layout()
plt.show()
```

**Análise:** `idxmax()` e `idxmin()` localizam os extremos de preço. `nlargest()` retorna os registros com os maiores valores de uma coluna. O gráfico de barras horizontal facilita a comparação visual do faturamento entre categorias.

## 6. Reflexão final

```python
# Insight interessante extraído dos dados
print("=== INSIGHTS ===")
print(f"- Preço médio dos livros: R$ {preco_medio:.2f}")
print(f"- Avaliação média geral: {avaliacao_media:.2f}")
print(f"- Categoria com maior faturamento: {categoria_maior_faturamento}")
print(f"- Categoria melhor avaliada: {melhor_categoria_avaliacao}")
print()
print("Um insight relevante: a categoria com maior faturamento não é necessariamente")
print("a mais vendida em unidades nem a melhor avaliada. Isso sugere que o preço")
print("impacta significativamente a receita. Livros com preço mais alto em categorias")
print("de nicho podem gerar mais receita do que best-sellers baratos. A livraria")
print("pode usar isso para otimizar seu mix de produtos e estratégia de precificação.")
```
