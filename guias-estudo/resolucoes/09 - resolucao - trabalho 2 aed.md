# Resolução — Trabalho 2: Análise do Dataset `tips`

## Parte 1: Carregamento e Inspeção dos Dados

```python
# Importa as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carrega o dataset tips.csv para um DataFrame
df = pd.read_csv("tips.csv")

# Exibe as 10 primeiras linhas para uma primeira inspeção
df.head(10)
"""
   total_bill   tip     sex smoker  day    time  size
0       16.99  1.01  Female     No  Sun  Dinner     2
1       10.34  1.66    Male     No  Sun  Dinner     3
2       21.01  3.50    Male     No  Sun  Dinner     3
3       23.68  3.31    Male     No  Sun  Dinner     2
4       24.59  3.61  Female     No  Sun  Dinner     4
5       25.29  4.71    Male     No  Sun  Dinner     4
6        8.77  2.00    Male     No  Sun  Dinner     2
7       26.88  3.12    Male     No  Sun  Dinner     4
8       15.04  1.96    Male     No  Sun  Dinner     2
9       14.78  3.23    Male     No  Sun  Dinner     2
"""

# Exibe informações estruturais: tipos, valores não-nulos, uso de memória
df.info()
"""
<class 'pandas.DataFrame'>
RangeIndex: 418 entries, 0 to 417
Data columns (total 7 columns):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   total_bill  418 non-null    float64
 1   tip         418 non-null    float64
 2   sex         418 non-null    str
 3   smoker      418 non-null    str
 4   day         418 non-null    str
 5   time        418 non-null    str
 6   size        418 non-null    int64
dtypes: float64(2), int64(1), str(4)
memory usage: 23.0 KB
"""

# Gera estatísticas descritivas das colunas numéricas
df.describe()
"""
       total_bill         tip        size
count  418.000000  418.000000  418.000000
mean    19.637871    2.997775    2.523923
std      8.515342    1.335773    0.859787
min      5.750000    1.000000    1.000000
25%     13.160000    2.000000    2.000000
50%     17.550000    3.000000    2.000000
75%     24.047500    3.550000    3.000000
max     50.810000   10.000000    6.000000
"""
```

### Pergunta Analítica (Parte 1):

Ao analisar a saída do `.info()` os dados parecem adequados para iniciar a análise. Todas as linhas têm valores não nulos e estão bem escritos (sem erros ortográficos ou valores semanticamente duplicados). No entanto, colunas como `sex` e `smoker` poderiam estar em formato categórico em vez de `string`.

Analisando o `.describe()` para `total_bill`: a média é ~19,6 e a mediana (50%) é ~17,5. Como são próximas, sugere que a maioria das contas tem valores semelhantes.

O nome da variável `sex` é ambíguo — não está claro se refere-se ao cliente ou ao atendente, pois não conhecemos a origem dos dados.

---

## Parte 2: Análise Univariada e Criação de Variável

```python
# Cria uma nova coluna: percentual da gorjeta em relação ao total da conta
df['tip_pct'] = df['tip'] / df['total_bill']

# Visualiza as primeiras linhas para confirmar a nova coluna
df.head()
"""
   total_bill   tip     sex smoker  day    time  size   tip_pct
0       16.99  1.01  Female     No  Sun  Dinner     2  0.059447
1       10.34  1.66    Male     No  Sun  Dinner     3  0.160542
2       21.01  3.50    Male     No  Sun  Dinner     3  0.166587
3       23.68  3.31    Male     No  Sun  Dinner     2  0.139780
4       24.59  3.61  Female     No  Sun  Dinner     4  0.146808
"""

# Verifica a frequência de clientes fumantes e não fumantes
print(df['smoker'].value_counts())
"""
smoker
No     260
Yes    158
Name: count, dtype: int64
"""

# Gráfico de contagem (countplot) para a variável 'day'
sns.countplot(df['day'])
plt.title('Distribuição de Refeições por Dia da Semana')
plt.show()
"""
Revela que Sábado (Sat) e Domingo (Sun) são os dias com maior movimento,
enquanto Sexta (Fri) tem o menor número de registros.
"""

# Histograma com curva de densidade para 'total_bill'
sns.histplot(df['total_bill'], kde=True)
plt.title('Distribuição do Valor Total da Conta')
plt.show()
"""
A distribuição é assimétrica à direita (cauda longa). A maioria das contas
concentra-se entre ~10 e ~25, com poucas contas acima de 40.
"""

# Dataframe ordenado pelos 10 maiores valores de 'total_bill' (nlargest)
df.nlargest(10, 'total_bill')
"""
     total_bill   tip     sex smoker day    time  size   tip_pct
152       50.81  10.0    Male    Yes  Sat  Dinner     3  0.196812
342       50.81  10.0    Male    Yes  Sat  Dinner     3  0.196812
56        48.17   5.0    Male     No  Sun  Dinner     6  0.103799
246       48.17   5.0    Male     No  Sun  Dinner     6  0.103799
170       45.35   3.5    Male    Yes  Sun  Dinner     3  0.077178
360       45.35   3.5    Male    Yes  Sun  Dinner     3  0.077178
141       44.30   2.5  Female    Yes  Sat  Dinner     3  0.056433
331       44.30   2.5  Female    Yes  Sat  Dinner     3  0.056433
118       43.11   5.0  Female    Yes  Thur  Lunch     4  0.115982
308       43.11   5.0  Female    Yes  Thur  Lunch     4  0.115982
"""

# Filtra linhas onde a gorjeta percentual ultrapassa 30%
percent_df = df[df['tip_pct'] > 0.30]
display(percent_df)
"""
     total_bill   tip   sex smoker  day    time  size   tip_pct
154        7.25  5.15  Male    Yes  Sun  Dinner     2  0.710345
344        7.25  5.15  Male    Yes  Sun  Dinner     2  0.710345
"""
```

### Perguntas Analíticas (Parte 2):

1. Os clientes que gastaram mais **não** foram os que deixaram as maiores gorjetas proporcionais.

2. Existem duas mesas consideradas atípicas (gorjeta > 30% do valor da conta). Observando os dados dos outliers, todos os valores são idênticos. Pode ser o mesmo cliente (fumante, sexo masculino, jantar de domingo), ou pode ser uma linha duplicada no dataset.

---

## Parte 3: Análise Bivariada (Relações)

```python
# Gráfico de dispersão: total_bill vs tip
sns.scatterplot(df, y='tip', x='total_bill')
plt.title('Relação entre Valor da Conta e Gorjeta')
plt.show()
"""
Observa-se uma correlação positiva forte: quanto maior o valor da conta,
maior a gorjeta em termos absolutos. A maioria dos pontos segue uma
tendência linear, sugerindo que as gorjetas são aproximadamente 15-20%
do total da conta.
"""

# Gráfico de barras: tip_pct médio por sexo
sns.barplot(df, x='sex', y='tip_pct')
plt.title('Percentual Médio de Gorjeta por Sexo')
plt.show()
"""
A diferença no percentual de gorjeta entre homens e mulheres é pequena
(~1%), indicando que o sexo do cliente não é um fator determinante
para a proporção da gorjeta.
"""

# Média da gorjeta absoluta agrupada por dia da semana
print(df.groupby('day')['tip'].mean())
"""
day
Fri     2.378182
Sat     3.079412
Sun     3.270993
Thur    2.767216
Name: tip, dtype: float64
"""
```

### Pergunta Analítica (Parte 3):

O gráfico de dispersão mostra uma relação forte entre valor da conta e gorjeta absoluta. A grande maioria das gorjetas parece ser de aproximadamente 15-20% do valor da conta.

O gráfico de barras por sexo mostra que não há diferença significativa na proporção de gorjeta entre homens e mulheres — a diferença é de aproximadamente 1%.

---

## Parte 4: Análise Multivariada e Síntese

```python
# Gráfico de dispersão total_bill vs tip, colorido por 'smoker'
sns.scatterplot(df, y='tip', x='total_bill', hue='smoker')
plt.title('Relação Conta vs Gorjeta (por Fumante/Não Fumante)')
plt.show()
"""
A cor (hue) revela que tanto fumantes quanto não fumantes seguem o mesmo
padrão de gorjeta. Não há uma separação clara entre os grupos — ambos
distribuem-se ao longo da mesma tendência linear.
"""

# Gráfico de barras do valor médio da gorjeta por dia, colorido por tipo de refeição
sns.barplot(df, x='day', y='tip', hue='time')
plt.title('Gorjeta Média por Dia e Tipo de Refeição')
plt.show()
"""
Os jantares (Dinner) têm gorjetas absolutas maiores que os almoços (Lunch)
em todos os dias. O domingo (Sun) e o sábado (Sat) destacam-se como os
dias de maior gorjeta, especialmente no jantar.
"""
```

### Pergunta Analítica (Parte 4) — Síntese de Insights:

- **Dias mais lucrativos para os garçons:** Finais de semana (Sábado e Domingo) e horário noturno (jantar) apresentam as maiores gorjetas absolutas. Estratégias de escala de funcionários podem priorizar esses períodos.

- **Fumantes vs Não fumantes:** O comportamento de gorjeta é semelhante entre os dois grupos, não havendo diferença significativa.

- **Sexo:** Homens e mulheres deixam valores percentuais de gorjeta muito próximos (~1% de diferença), indicando que não é um fator relevante.

- **Padrão geral:** Gorjetas absolutas maiores ocorrem no período noturno, provavelmente porque as contas totais tendem a ser mais altas no jantar. A relação entre total_bill e tip é consistente e aproximadamente linear.

- **Recomendação prática:** Para reter funcionários, a gerência pode escalar mais garçons nos jantares de finais de semana, onde as gorjetas são maiores.
