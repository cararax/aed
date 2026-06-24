# Machine Learning — Guia Rápido para a Prova

> 🎯 **Foco**: Classificação Supervisionada com Árvore de Decisão + scikit-learn
> Baseado nos notebooks: [`08 - Machine Learning/`](../08%20-%20Machine%20Learning/)

---

## Sumário

- [Pipeline ML — Passo a Passo](#pipeline-ml--passo-a-passo)
- [Quick Reference — Código Mínimo](#quick-reference--código-mínimo)
- [Explicação Detalhada](#explicação-detalhada)
  - [1. Carregar Dados](#1-carregar-dados)
  - [2. Separar Features (X) e Target (y)](#2-separar-features-x-e-target-y)
  - [3. Codificar Variáveis Categóricas](#3-codificar-variáveis-categóricas)
  - [4. Dividir em Treino e Teste](#4-dividir-em-treino-e-teste)
  - [5. Instanciar o Modelo](#5-instanciar-o-modelo)
  - [6. Treinar o Modelo](#6-treinar-o-modelo)
  - [7. Fazer Previsões](#7-fazer-previsões)
  - [8. Avaliar o Modelo](#8-avaliar-o-modelo)
  - [9. Visualizar a Árvore](#9-visualizar-a-árvore)
  - [10. Overfitting e Poda (Pruning)](#10-overfitting-e-poda-pruning)
- [Comparação de Modelos](#comparação-de-modelos)
- [Tabela de Métricas](#tabela-de-métricas)
- [Deploy / Inferência em Tempo Real](#deploy--inferência-em-tempo-real)
- [Exercícios Resolvidos](#exercícios-resolvidos)

---

## Pipeline ML — Passo a Passo

```
Carregar dados (CSV, sklearn dataset)
    ↓
Separar X (features) e y (target)
    ↓
Codificar colunas categóricas (se houver)
    ↓
Dividir em treino e teste (train_test_split)
    ↓
Instanciar modelo (DecisionTreeClassifier, etc.)
    ↓
Treinar (fit)
    ↓
Prever (predict)
    ↓
Avaliar (accuracy, confusion_matrix, precision, recall, f1)
    ↓
Visualizar (plot_tree, heatmap)
```

---

## Quick Reference — Código Mínimo

```python
# 1. Imports
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# 2. Carregar dados
df = pd.read_csv("arquivo.csv")

# 3. Separar X e y
X = df[['coluna1', 'coluna2', 'coluna3']]   # features
y = df['target']                              # alvo

# 4. Codificar categóricas (se necessário)
df['Genero'] = df['Genero'].map({'Female': 0, 'Male': 1})

# 5. Split treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 6. Criar e treinar modelo
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)

# 7. Prever
y_pred = modelo.predict(X_test)

# 8. Avaliar
acuracia = accuracy_score(y_test, y_pred)
print(f"Acurácia: {acuracia:.2f}")

matriz = confusion_matrix(y_test, y_pred)
print(matriz)
```

---

## Explicação Detalhada

### 1. Carregar Dados

**De CSV (pandas):**
```python
import pandas as pd
df = pd.read_csv("Social_Network_Ads.csv")
df.head()        # ver primeiras 5 linhas
df.info()        # estrutura: colunas, tipos, nulos
df.describe()    # estatísticas descritivas
```

**Do sklearn (dataset embutido):**
```python
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data          # array numpy com features
y = iris.target         # array numpy com classes
iris.feature_names      # ['sepal length', 'sepal width', ...]
iris.target_names       # ['setosa', 'versicolor', 'virginica']
```

> 📁 Arquivos originais: [`06 - Dados - Social Network Ads.csv`](../08%20-%20Machine%20Learning/06%20-%20Dados%20-%20Social%20Network%20Ads.csv),
> [`10 - Dados - Logs Ecommerce.csv`](../08%20-%20Machine%20Learning/10%20-%20Dados%20-%20Logs%20Ecommerce.csv)

---

### 2. Separar Features (X) e Target (y)

```python
# X = todas as colunas que "explicam" o resultado
# y = coluna que queremos prever

X = df[['Age', 'EstimatedSalary']]   # DataFrame com as features
y = df['Purchased']                   # Series com o target (0 ou 1)
```

🧠 **Regra prática**: features são sempre **números**. Se tem texto, precisa codificar (passo 3).

---

### 3. Codificar Variáveis Categóricas

Modelos de ML não entendem texto — só números.

```python
# Método 1: .map() para 2 categorias
df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1})

# Método 2: get_dummies() para N categorias
df = pd.get_dummies(df, columns=['cor'], drop_first=True)
```

> Exemplo real no notebook [`08 - Gabarito - Social Network Ads.ipynb`](../08%20-%20Machine%20Learning/08%20-%20Gabarito%20-%20Social%20Network%20Ads.ipynb)

---

### 4. Dividir em Treino e Teste

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,        # 30% para teste, 70% para treino
    random_state=42,      # seed para reprodutibilidade
    stratify=y            # manter proporção das classes (importante!)
)
```

| Parâmetro | O que faz |
|-----------|-----------|
| `test_size=0.3` | 30% dos dados viram teste |
| `random_state=42` | Fixa a "semente" — resultados reproduzíveis |
| `stratify=y` | Mantém a mesma proporção de classes no treino e teste |
| `train_size=0.7` | Alternativa: 70% treino |

📏 **Tamanhos comuns**: 70/30, 80/20, 90/10 (quanto mais dados, maior a % de treino).

---

### 5. Instanciar o Modelo

```python
from sklearn.tree import DecisionTreeClassifier

# Modelo básico (pode overfitting)
modelo = DecisionTreeClassifier(random_state=42)

# Modelo com poda (pruning) — evita overfitting
modelo = DecisionTreeClassifier(max_depth=3, random_state=42)

# Modelo com critério de entropia
modelo = DecisionTreeClassifier(criterion='entropy', max_depth=9, random_state=42)
```

| Parâmetro | Padrão | O que faz |
|-----------|--------|-----------|
| `random_state` | None | Reprodutibilidade |
| `max_depth` | None | Profundidade máxima da árvore (quanto maior, mais overfitting) |
| `criterion` | `'gini'` | Função para medir qualidade da divisão (`'gini'` ou `'entropy'`) |
| `min_samples_split` | 2 | Mínimo de amostras para dividir um nó |
| `min_samples_leaf` | 1 | Mínimo de amostras em cada folha |

> 📁 Notebook original: [`03 - Exemplo 1 - Iris - Arvore Decisao Basico.ipynb`](../08%20-%20Machine%20Learning/03%20-%20Exemplo%201%20-%20Iris%20-%20Arvore%20Decisao%20Basico.ipynb)

---

### 6. Treinar o Modelo

```python
modelo.fit(X_train, y_train)
# O modelo "aprende" os padrões dos dados de treino
```

O método `.fit()` é onde o **aprendizado** acontece. A árvore decide quais perguntas fazer e em que ordem, baseada nos dados de treino.

---

### 7. Fazer Previsões

```python
y_pred = modelo.predict(X_test)           # classes: 0 ou 1
y_proba = modelo.predict_proba(X_test)    # probabilidades: [P(0), P(1)]
```

| Método | Retorna | Exemplo |
|--------|---------|---------|
| `.predict(X)` | Array com as classes previstas | `[0, 1, 0, 0, 1]` |
| `.predict_proba(X)` | Array com probabilidades | `[[0.95, 0.05], [0.10, 0.90]]` |

🧠 `predict_proba` é útil para **medir a confiança** do modelo na previsão.

---

### 8. Avaliar o Modelo

```python
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)
```

#### Acurácia
```python
acuracia = accuracy_score(y_test, y_pred)
# Percentual de acertos no teste
```

#### Matriz de Confusão
```python
cm = confusion_matrix(y_test, y_pred)
print(cm)
# [[24  2]     → VP=24, FN=2
#  [ 4 10]]    → FP=4, VN=10

# Visualização com heatmap
import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Matriz de Confusão")
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.show()
```

#### Precision, Recall, F1-Score
```python
# Por classe
precision = precision_score(y_test, y_pred, average=None)
recall = recall_score(y_test, y_pred, average=None)
f1 = f1_score(y_test, y_pred, average=None)

# Média ponderada (weighted)
precision_media = precision_score(y_test, y_pred, average='weighted')
recall_media = recall_score(y_test, y_pred, average='weighted')
f1_media = f1_score(y_test, y_pred, average='weighted')
```

> 📁 Notebook original: [`05 - Exemplo 3 - Iris - Metricas Avaliacao.ipynb`](../08%20-%20Machine%20Learning/05%20-%20Exemplo%203%20-%20Iris%20-%20Metricas%20Avaliacao.ipynb)

---

### 9. Visualizar a Árvore

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plot_tree(modelo,
          feature_names=X.columns,            # nomes das colunas
          class_names=["Não Comprou", "Comprou"],  # nomes das classes
          filled=True,                         # cores por classe
          rounded=True)
plt.title("Árvore de Decisão")
plt.show()
```

A visualização da árvore permite **entender as regras** que o modelo aprendeu:
- Cada nó mostra: condição, gini/entropy, amostras, valor, classe majoritária
- Cores mais escuras = maior pureza (certeza)

---

### 10. Overfitting e Poda (Pruning)

**Overfitting** = modelo decora os dados de treino mas não generaliza para novos dados.

**Como detectar:**
```python
train_pred = modelo.predict(X_train)
train_acc = accuracy_score(y_train, train_pred)
test_acc = accuracy_score(y_test, y_pred)

print(f"Acurácia TREINO: {train_acc:.2f}")   # ex: 1.00
print(f"Acurácia TESTE: {test_acc:.2f}")     # ex: 0.85

if train_acc > test_acc + 0.05:
    print("⚠️  Possível overfitting!")
```

**Como resolver — Poda (pruning):**
```python
# Reduzir a profundidade máxima
modelo_podado = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo_podado.fit(X_train, y_train)
```

> 📁 Notebook original: [`04 - Exemplo 2 - Iris - Comparacao Modelos.ipynb`](../08%20-%20Machine%20Learning/04%20-%20Exemplo%202%20-%20Iris%20-%20Comparacao%20Modelos.ipynb)

---

## Comparação de Modelos

| Modelo | Classe sklearn | Quando usar |
|--------|---------------|-------------|
| **Árvore de Decisão** | `DecisionTreeClassifier` | Interpretável, fácil de explicar |
| **K-NN** | `KNeighborsClassifier(n_neighbors=5)` | Dados pequenos, limites não-lineares |
| **Regressão Logística** | `LogisticRegression()` | Limite linear, probabilidades calibradas |
| **LDA** | `LinearDiscriminantAnalysis()` | Classes bem separáveis, normalidade |
| **Naive Bayes** | `GaussianNB()` | Muitas features, independência entre elas |
| **SVM** | `SVC()` | Limites complexos, dados médios |

```python
# Importar todos de uma vez
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Dicionário de modelos
modelos = {
    "Árvore de Decisão": DecisionTreeClassifier(max_depth=3, random_state=42),
    "K-NN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Regressão Logística": LogisticRegression(random_state=42, max_iter=200),
    "LDA": LinearDiscriminantAnalysis(),
    "Naive Bayes": GaussianNB(),
    "SVM": SVC(random_state=42)
}

# Comparar todos
for nome, model in modelos.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    print(f"{nome}: {acc:.2f}")
```

---

## Tabela de Métricas

| Métrica | Fórmula | O que mede | `average=` |
|---------|---------|------------|------------|
| **Acurácia** | `(VP+VN) / total` | % de acertos geral | — |
| **Precisão** | `VP / (VP+FP)` | Das que preví como positivas, quantas eram mesmo | `'weighted'` |
| **Recall** | `VP / (VP+FN)` | Das que eram positivas, quantas eu acertei | `'weighted'` |
| **F1-Score** | `2 * (P * R) / (P + R)` | Média harmônica entre precisão e recall | `'weighted'` |

```
              Real: Sim   Real: Não
Previsto Sim     VP          FP
Previsto Não     FN          VN
```

- **VP** (Verdadeiro Positivo): acertou que é positivo
- **VN** (Verdadeiro Negativo): acertou que é negativo
- **FP** (Falso Positivo): disse que é positivo, mas era negativo
- **FN** (Falso Negativo): disse que é negativo, mas era positivo

> `average='weighted'` calcula a média ponderada pelo número de amostras de cada classe.
> `average=None` retorna o valor de cada classe separadamente.

---

## Deploy / Inferência em Tempo Real

Simular o modelo em produção com novos dados:

```python
# Novos dados simulados (como se viessem de uma API)
novos_usuarios = [
    {"usuario": "João", "paginas_visitadas": 2, "tempo_site_min": 1.5, "adicionou_carrinho": 0},
    {"usuario": "Maria", "paginas_visitadas": 8, "tempo_site_min": 12.0, "adicionou_carrinho": 1}
]

# Converter para DataFrame
df_novos = pd.DataFrame(novos_usuarios)
X_novos = df_novos[['paginas_visitadas', 'tempo_site_min', 'adicionou_carrinho']]

# Prever
previsoes = modelo.predict(X_novos)
probabilidades = modelo.predict_proba(X_novos)

for i, row in df_novos.iterrows():
    status = "🛒 ALTA CHANCE" if previsoes[i] == 1 else "👀 BAIXA CHANCE"
    prob = probabilidades[i][1] * 100
    print(f"{row['usuario']}: {status} (certeza: {prob:.1f}%)")
```

> 📁 Notebook original: [`09 - Exemplo - Ecommerce Implantacao.ipynb`](../08%20-%20Machine%20Learning/09%20-%20Exemplo%20-%20Ecommerce%20Implantacao.ipynb)

---

## Checklist para a Prova

Antes de entregar, verifique:

- [ ] Dados carregados corretamente (`.head()`, `.info()`)
- [ ] Colunas categóricas foram codificadas
- [ ] `X` e `y` estão separados
- [ ] Split treino/teste feito com `stratify` (classificação)
- [ ] Modelo instanciado com `random_state` para reprodutibilidade
- [ ] Modelo treinado (`.fit()`)
- [ ] Previsões feitas (`.predict()`)
- [ ] Acurácia calculada
- [ ] Matriz de confusão gerada
- [ ] (Opcional) Precision/Recall/F1 calculados
- [ ] Árvore visualizada (se for árvore de decisão)
- [ ] Comentários explicando cada etapa

---

## Exercícios Resolvidos

| Exercício | Resolução |
|-----------|-----------|
| 🧪 Social Network Ads — Classificação | [📄 Resolução comentada](resolucoes/07%20-%20resolucao%20-%20social%20network%20ads.md) |
| 🛒 E-commerce — Implantação | [📄 Resolução comentada](resolucoes/08%20-%20resolucao%20-%20ecommerce%20implantacao.md) |

---

> 📎 **Arquivos originais da disciplina**: pasta [`08 - Machine Learning/`](../08%20-%20Machine%20Learning/)
> 📚 **Materiais de apoio**: [`00 - Materiais De Apoio/03 - Python Para Todos - Severance.pdf`](../00%20-%20Materiais%20De%20Apoio/03%20-%20Python%20Para%20Todos%20-%20Severance.pdf) (cap. 11-16)
