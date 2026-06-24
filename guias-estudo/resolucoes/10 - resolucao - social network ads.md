# Resolução - Classificação com Social Network Ads

## 1. Importação das Bibliotecas

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
```

- **pandas**: manipulação e análise de dados em formato tabular (DataFrame).
- **train_test_split**: divide os dados em conjuntos de treino e teste.
- **DecisionTreeClassifier**: implementa o algoritmo de árvore de decisão para classificação.
- **plot_tree**: visualiza graficamente a estrutura da árvore treinada.
- **accuracy_score / confusion_matrix**: métricas para avaliar o desempenho do modelo.

---

## 2. Carregamento e Exploração dos Dados

```python
df = pd.read_csv("Social_Network_Ads.csv")
df.head()
```

| User ID | Gender | Age | EstimatedSalary | Purchased |
|---------|--------|-----|-----------------|-----------|
| 15624510 | Male | 19 | 19000 | 0 |
| 15810944 | Male | 35 | 20000 | 0 |
| 15668575 | Female | 26 | 43000 | 0 |
| 15603246 | Female | 27 | 57000 | 0 |
| 15804002 | Male | 19 | 76000 | 0 |

O dataset contém **400 registros** de usuários de redes sociais com informações demográficas e comportamentais. A coluna `Purchased` (0 ou 1) indica se o usuário comprou um produto após ver um anúncio — este é o nosso **alvo (target)**.

### Por que precisamos pré-processar a coluna Gender?

A coluna `Gender` contém valores categóricos textuais (`"Male"` / `"Female"`). Modelos de Machine Learning, incluindo árvores de decisão no scikit-learn, **não aceitam dados categóricos em formato texto diretamente**. É necessário **codificar** essas categorias em valores numéricos. A técnica mais simples é o **label encoding**: atribuir um inteiro distinto para cada categoria.

```python
df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1})
```

| User ID | Gender | Age | EstimatedSalary | Purchased |
|---------|--------|-----|-----------------|-----------|
| 0 | 1 | 19 | 19000 | 0 |
| 1 | 1 | 35 | 20000 | 0 |
| 2 | 0 | 26 | 43000 | 0 |
| 3 | 0 | 27 | 57000 | 0 |
| 4 | 1 | 19 | 76000 | 0 |

Agora `Female = 0` e `Male = 1`, valores numericamente interpretáveis pelo modelo.

---

## 3. Separação entre Features (X) e Target (y)

```python
X = df[['Gender', 'Age', 'EstimatedSalary']]
y = df['Purchased']
```

- **X** (matriz de características): as variáveis que o modelo usará para fazer a predição.
- **y** (vetor alvo): o que queremos prever (comprou ou não comprou).

> A coluna `User ID` é **excluída** porque é um identificador único sem poder preditivo — incluí-la causaria overfitting (o modelo decoraria IDs em vez de aprender padrões).

---

## 4. Divisão Treino-Teste com Estratificação

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y
)
```

- **90% treino (360 amostras)**, **10% teste (40 amostras)**.
- `random_state=42`: garante reprodutibilidade (sempre a mesma divisão).
- `stratify=y`: essencial em problemas de **classificação com classes desbalanceadas**. Garante que a proporção de classes no treino e no teste seja a mesma do dataset original. Sem stratify, um split aleatório poderia, por azar, deixar o teste sem amostras da classe minoritária.

---

## 5. Treinamento da Árvore de Decisão

```python
modelo = DecisionTreeClassifier(
    random_state=42, max_depth=9, criterion='entropy'
)
modelo.fit(X_train, y_train)
```

### O que é o critério `entropy`?

O **critério de entropia** mede o **grau de impureza/desordem** de um conjunto de dados. A árvore decide por onde dividir os dados escolhendo o atributo que **mais reduz a entropia** (ou seja, que maximiza o **ganho de informação**).

- **Entropia = 0**: conjunto perfeitamente puro (todos pertencem à mesma classe).
- **Entropia = 1**: conjunto perfeitamente misturado (50%/50%).

A fórmula da entropia para uma variável binária é:

```
Entropia(S) = -p+ * log2(p+) - p- * log2(p-)
```

O algoritmo testa todas as features e todos os pontos de corte possíveis, escolhendo aquele que resulta na **maior redução de entropia** (Information Gain).

> Alternativa comum: `criterion='gini'` (índice Gini). Ambos produzem resultados similares na prática; a entropia tende a gerar árvores ligeiramente mais equilibradas.

### Por que `max_depth=9`?

**Limitar a profundidade** (`max_depth`) é uma forma de **poda (pruning)** que previne overfitting. Uma árvore sem limite de profundidade pode crescer até que cada folha contenha uma única amostra, decorando o ruído dos dados de treino em vez de aprender o padrão geral. O valor 9 foi escolhido empiricamente para este dataset.

---

## 6. Avaliação do Modelo

```python
y_pred = modelo.predict(X_test)

acuracia = accuracy_score(y_test, y_pred)
print(f"Acurácia: {acuracia:.2f}")
# Saída: Acurácia: 0.85

matriz = confusion_matrix(y_test, y_pred)
print(matriz)
# Saída: [[24  2]
#         [ 4 10]]
```

### Interpretação da Matriz de Confusão

A matriz de confusão confronta os valores **reais** (linhas) com os **previstos** (colunas):

```
              Previsto
              0    1
Real  0  [[ 24,  2 ],    → 24 corretos (VN), 2 falsos positivos (FP)
      1   [  4,  10 ]]   → 4 falsos negativos (FN), 10 corretos (VP)
```

| Termo | Significado | Neste caso |
|-------|-------------|------------|
| **VN (Verdadeiro Negativo)** | Modelo acertou que NÃO comprou | 24 |
| **FP (Falso Positivo)** | Modelo errou: disse que compraria mas não comprou | 2 |
| **FN (Falso Negativo)** | Modelo errou: disse que não compraria mas comprou | 4 |
| **VP (Verdadeiro Positivo)** | Modelo acertou que comprou | 10 |

**Acurácia = (24 + 10) / (24 + 2 + 4 + 10) = 34 / 40 = 0.85 (85%)**

O modelo é eficaz, mas erra mais em **falsos negativos** (4 casos) do que em **falsos positivos** (2 casos) — tende a subestimar a intenção de compra.

---

## 7. Visualização da Árvore de Decisão

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
plot_tree(
    modelo,
    feature_names=['Gender', 'Age', 'EstimatedSalary'],
    class_names=['Não Comprou', 'Comprou'],
    filled=True,
    rounded=True,
    fontsize=10
)
plt.show()
```

### Como ler a árvore de decisão

Cada **nó interno** da árvore contém:

1. **Condição de divisão**: ex. `Age <= 34.5` — se verdadeiro, vai para o ramo da esquerda; se falso, para a direita.
2. **Entropia** do nó: quão misturadas estão as classes naquele grupo.
3. **Número de amostras** (`samples`): quantos registros de treino chegaram até aquele nó.
4. **Distribuição de classes** (`value`): ex. `[120, 30]` significa 120 não-compradores e 30 compradores.

Os **nós folha** (terminais) contêm a decisão final. A cor reflete a classe majoritária (azul para uma classe, laranja para a outra), com a intensidade indicando o grau de pureza.

<img src="https://scikit-learn.org/stable/_images/iris.png" alt="Exemplo de árvore de decisão" width="600"/>

A árvore resultante mostra que **Age** e **EstimatedSalary** são as features mais importantes para a decisão de compra, enquanto **Gender** tem menor influência (pode nem aparecer nos primeiros níveis).

---

## Conclusão

- Conseguimos um modelo com **85% de acurácia** na predição de compra de anúncios.
- A árvore de decisão revela que **faixa etária** e **salário estimado** são os principais fatores determinantes.
- A estratificação garantiu que a avaliação fosse justa, mantendo a proporção de classes.
- A codificação de variáveis categóricas foi necessária para o funcionamento do algoritmo.
- O uso de entropia como critério de divisão busca maximizar a pureza das folhas a cada passo.
