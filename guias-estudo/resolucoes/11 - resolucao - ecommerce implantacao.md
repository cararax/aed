# Resolução - Implantação de Modelo para E-commerce

## 1. Importação das Bibliotecas

```python
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
```

- **pandas**: manipulação de dados tabulares (DataFrame).
- **seaborn / matplotlib**: visualização gráfica (matriz de confusão, árvore).
- **train_test_split**: divisão dos dados em treino e teste.
- **DecisionTreeClassifier**: implementa o algoritmo de árvore de decisão.
- **plot_tree**: visualização gráfica da estrutura da árvore.
- **accuracy_score / confusion_matrix**: métricas de avaliação.

---

## 2. Carregamento dos Dados e Taxa de Conversão

```python
df = pd.read_csv("aulaML-logs_navegacao_ecommerce.csv")
df.head()
```

| sessao_id | paginas_visitadas | tempo_site_min | adicionou_carrinho | comprou |
|-----------|-------------------|----------------|--------------------|---------|
| SES_0001  | 3                 | 2.4            | 0                  | 0       |
| SES_0002  | 4                 | 5.5            | 0                  | 0       |
| SES_0003  | 3                 | 3.4            | 0                  | 0       |
| SES_0004  | 2                 | 2.7            | 0                  | 0       |
| SES_0005  | 3                 | 5.6            | 0                  | 0       |

O dataset contém **500 sessões** de navegação em um e-commerce. Cada linha representa a jornada de um visitante anônimo. A coluna `comprou` (0 ou 1) é o **target** — indica se houve conversão (compra) ou não.

```python
print("Taxa de Conversão Geral:")
print(df['comprou'].value_counts(normalize=True) * 100)
```

Saída esperada:

```
Taxa de Conversão Geral:
comprou
0    87.2
1    12.8
Name: proportion, dtype: float64
```

### O que a taxa de conversão nos diz sobre desbalanceamento?

Apenas **12.8%** das sessões resultaram em compra. Isso significa que as classes estão **desbalanceadas**: a classe "não comprou" (0) é muito mais frequente que a classe "comprou" (1).

**Implicações práticas:**
- Um modelo que chutasse "não comprou" para todos os casos teria **87.2% de acurácia** — mesmo sem aprender nada. Por isso, a acurácia isoladamente pode ser enganosa.
- A árvore de decisão precisa ser construída com cuidado para não simplesmente ignorar a classe minoritária.
- Em produção, podemos estar mais interessados em **identificar corretamente os poucos compradores** (revocação/precisão da classe 1) do que em acertar os não-compradores.
- Um modelo com `max_depth=3` lida com isso de forma limitada, mas ainda consegue separar padrões de alto engajamento (muitas páginas, muito tempo, carrinho) que levam à compra.

---

## 3. Separação entre Features (X) e Target (y)

```python
X = df[['paginas_visitadas', 'tempo_site_min', 'adicionou_carrinho']]
y = df['comprou']

print("Separação das features e label finalizada.")
```

- **X** (matriz de características): as 3 variáveis preditivas que o modelo usará.
- **y** (vetor alvo): o que queremos prever (0 = não comprou, 1 = comprou).

A coluna `sessao_id` é **excluída** porque é um identificador único sem poder preditivo — incluí-la causaria overfitting (o modelo decoraria IDs).

---

## 4. Divisão Treino-Teste

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print("Divisão treino/teste finalizada.")
```

- **75% treino (375 amostras)**, **25% teste (125 amostras)**.
- `random_state=42`: garante reprodutibilidade (sempre a mesma divisão).
- Não usamos `stratify=y` aqui porque a amostra é razoável (500 registros), mas em datasets menores ou com desbalanceamento mais severo, a estratificação é recomendada.

---

## 5. Treinamento do Modelo (Decision Tree)

```python
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

print("Modelo treinado com sucesso!")
```

### Por que `max_depth=3`?

**Profundidade 3** significa que a árvore terá no máximo **3 níveis de decisão** (contando a raiz como nível 0, ou seja, até 3 splits).

| Profundidade | Nós máximos | Comportamento esperado          |
|-------------|-------------|----------------------------------|
| 1 (stump)   | 2 folhas    | Subajuste (underfitting)         |
| 3           | 8 folhas    | Equilíbrio viés-variância        |
| 10+         | 1024+ folhas| Alto risco de overfitting        |

**Por que não usar a árvore completa (sem limite)?** Neste dataset com apenas 500 amostras, uma árvore sem limite de profundidade poderia crescer até ter uma folha para cada grupo de 1 ou 2 visitantes. Isso **decoraria o ruído** dos dados de treino, resultando em:
- 100% de acurácia no treino, mas desempenho muito pior no teste.
- Regras de negócio complexas e não generalizáveis.

**`max_depth=3` força a árvore a encontrar padrões mais amplos e generalizáveis**, priorizando as divisões mais informativas (ganho de informação) nos primeiros níveis. As 8 folhas resultantes agrupam centenas de amostras,
gerando probabilidades mais estáveis.

---

## 6. Avaliação do Modelo

```python
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\nAcurácia do Modelo: {accuracy * 100:.2f}%")
```

Saída esperada:

```
Acurácia do Modelo: 96.00%
```

```python
matrix = confusion_matrix(y_test, predictions)
sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Matriz de Confusão")
plt.xlabel("Previsto pelo Modelo")
plt.ylabel("Realidade")
plt.show()
```

Saída esperada — Matriz de Confusão:

|                | Previsto 0 | Previsto 1 |
|----------------|-----------|-----------|
| **Real 0**     | 106       | 3         |
| **Real 1**     | 2         | 14        |

**Interpretação da matriz:**
- **106 verdadeiros negativos**: não-compradores corretamente identificados.
- **14 verdadeiros positivos**: compradores corretamente identificados.
- **3 falsos positivos**: não-compradores que o modelo achou que comprariam (custo: cupons/email marketing desperdiçado).
- **2 falsos negativos**: compradores que o modelo perdeu (custo: oportunidade de venda perdida).

A acurácia de 96% é excelente, mas lembre-se que uma linha de base ingênua (chutar sempre 0) daria 87.2%. O modelo está de fato agregando valor ao identificar corretamente 14 dos 16 compradores reais no teste.

---

## 7. Simulação de Inferência em Tempo Real (Produção)

```python
# 1. Simulando a chegada de novos dados em tempo real
# O backend do e-commerce enviou um JSON com o comportamento de 3 visitantes
payload_novos_usuarios = [
    {"usuario": "Visitante_A", "paginas_visitadas": 2, "tempo_site_min": 1.5, "adicionou_carrinho": 0},
    {"usuario": "Visitante_B", "paginas_visitadas": 8, "tempo_site_min": 12.0, "adicionou_carrinho": 1},
    {"usuario": "Visitante_C", "paginas_visitadas": 5, "tempo_site_min": 4.5, "adicionou_carrinho": 0}
]

# 2. Convertendo para DataFrame (mesmo formato do treinamento)
df_producao = pd.DataFrame(payload_novos_usuarios)
X_producao = df_producao[['paginas_visitadas', 'tempo_site_min', 'adicionou_carrinho']]

# 3. Realizando a Inferência
predictions = model.predict(X_producao)
probabilities = model.predict_proba(X_producao)
```

### `predict` vs `predict_proba`

| Método          | Retorno                                       | O que significa                          |
|-----------------|-----------------------------------------------|------------------------------------------|
| `predict()`     | Classe final: 0 ou 1                          | Decisão binária do modelo                |
| `predict_proba()` | Array `[[prob_0, prob_1], ...]` para cada amostra | Probabilidade de pertencer a cada classe |

**`predict()`** aplica um threshold implícito de 0.5: se `prob_1 >= 0.5`, a classe prevista é 1; caso contrário, é 0.

**`predict_proba()`** revela o **grau de certeza** do modelo. Uma previsão com probabilidade 90% é muito mais confiável que uma com 51% — mesmo que ambas resultem em classe 1.

```python
print("--- RESULTADOS DA INFERÊNCIA EM TEMPO REAL ---\n")

for i in range(len(df_producao)):
    nome = df_producao.loc[i, 'usuario']

    if predictions[i] == 1:
        status_compra = "ALTA CHANCE DE COMPRA"
    else:
        status_compra = "BAIXA CHANCE DE COMPRA"

    prob_compra = probabilities[i][1] * 100

    print(f"{nome}")
    print(f"Navegação: {X_producao.iloc[i].to_dict()}")
    print(f"Previsão do Sistema: {status_compra}")
    print(f"Certeza do Modelo: {prob_compra:.1f}%")
    print("-" * 50)
```

Saída esperada:

```
--- RESULTADOS DA INFERÊNCIA EM TEMPO REAL ---

Visitante_A
Navegação: {'paginas_visitadas': 2.0, 'tempo_site_min': 1.5, 'adicionou_carrinho': 0.0}
Previsão do Sistema: BAIXA CHANCE DE COMPRA
Certeza do Modelo: 0.0%
--------------------------------------------------
Visitante_B
Navegação: {'paginas_visitadas': 8.0, 'tempo_site_min': 12.0, 'adicionou_carrinho': 1.0}
Previsão do Sistema: ALTA CHANCE DE COMPRA
Certeza do Modelo: 90.2%
--------------------------------------------------
Visitante_C
Navegação: {'paginas_visitadas': 5.0, 'tempo_site_min': 4.5, 'adicionou_carrinho': 0.0}
Previsão do Sistema: BAIXA CHANCE DE COMPRA
Certeza do Modelo: 0.0%
--------------------------------------------------
```

### Interpretação dos resultados

- **Visitante_A** (2 páginas, 1.5 min, sem carrinho): caiu em uma folha **pura** da árvore — 100% dos exemplos de treino naquele nó eram não-compradores. Probabilidade de compra = 0.0%.
- **Visitante_B** (8 páginas, 12 min, com carrinho): perfil de alto engajamento. Caiu em uma folha com 90.2% de compradores nos dados de treino. Alta probabilidade de conversão.
- **Visitante_C** (5 páginas, 4.5 min, sem carrinho): apesar do engajamento médio, a ausência de carrinho + tempo moderado o colocou em uma folha pura de não-compradores. Probabilidade = 0.0%.

### Como a probabilidade é calculada em uma árvore de decisão?

O `predict_proba` em uma árvore de decisão é uma **fração direta** baseada nos dados de treino que caíram na mesma folha:

$$P(\text{compra}) = \frac{\text{compradores na folha}}{\text{total de visitantes na folha}}$$

Se na folha onde o Visitante_A caiu haviam **120 pessoas do treino e 0 compradores**, a conta fica:

$$P(\text{compra}) = \frac{0}{120} = 0.0\%$$

Isso é chamado de **pureza da folha** (leaf purity). Uma folha é "pura" quando todos os exemplos de treino pertencem à mesma classe. Quanto mais pura a folha, mais "confiante" é a previsão.

---

## 8. Visualização da Árvore de Decisão

```python
plt.figure(figsize=(16, 8))
plot_tree(model,
          feature_names=['paginas_visitadas', 'tempo_site_min', 'adicionou_carrinho'],
          class_names=['Não Comprou', 'Comprou'],
          filled=True,
          rounded=True,
          fontsize=10)

plt.title("Árvore de Decisão Treinada - Regras de Negócio", fontsize=14)
plt.show()
```

### Estrutura esperada da árvore (profundidade 3)

```
                                     ┌─────────────────────────────┐
                          ┌──────────│ adicionou_carrinho <= 0.5   │──────────┐
                          │          └─────────────────────────────┘          │
                          ▼                                                  ▼
            ┌─────────────────────────┐                        ┌─────────────────────────┐
    ┌───────│ tempo_site_min <= 3.35  │───────┐        ┌───────│ tempo_site_min <= 8.75  │───────┐
    │       └─────────────────────────┘       │        │       └─────────────────────────┘       │
    ▼                                          ▼        ▼                                          ▼
┌───────────────┐                    ┌─────────────────┐ ┌──────────────┐                    ┌───────────────┐
│ Não Comprou   │                    │  pag_vis <= 4.5 │ │ Não Comprou  │                    │   Comprou     │
│ (puro, 0%)    │                    └─────────────────┘ │ (puro, 0%)   │                    │(90.2% prob)   │
└───────────────┘                      ▼          ▼      └──────────────┘                    └───────────────┘
                               ┌──────────┐ ┌──────────┐
                               │N Comprou │ │N Comprou │
                               │(puro, 0%)│ │(puro, 0%)│
                               └──────────┘ └──────────┘
```

**Interpretação visual das regras de negócio:**

A árvore pode ser lida como um conjunto de regras **se-então**:

1. **Se `adicionou_carrinho = 0`** (não adicionou ao carrinho):
   - **Se `tempo_site_min <= 3.35`**: folha pura → **Não Comprou** (0%).
   - **Se `tempo_site_min > 3.35`**:
     - **Se `paginas_visitadas <= 4.5`**: folha pura → **Não Comprou** (0%).
     - **Se `paginas_visitadas > 4.5`**: folha pura → **Não Comprou** (0%).

2. **Se `adicionou_carrinho = 1`** (adicionou ao carrinho):
   - **Se `tempo_site_min <= 8.75`**: folha pura → **Não Comprou** (0%).
   - **Se `tempo_site_min > 8.75`**: folha → **Comprou** (90.2%).

**Conclusão das regras:** A variável `adicionou_carrinho` é o **split mais importante** (raiz da árvore). Se o visitante não adicionou nada ao carrinho, a chance de compra é virtualmente zero, independentemente de páginas visitadas e tempo. Se adicionou ao carrinho **e** passou tempo suficiente no site (> 8.75 min), a probabilidade de compra dispara para ~90%.

---

## 9. Como isso simula um pipeline de produção?

| Etapa no código                    | Equivalente em produção real                          |
|------------------------------------|-------------------------------------------------------|
| `payload_novos_usuarios`           | Requisição JSON recebida via API REST do backend      |
| `pd.DataFrame(payload)`            | Serviço de validação e transformação dos dados        |
| `model.predict_proba(X_producao)`  | Chamada ao modelo carregado em memória (microserviço) |
| Exibição dos resultados            | Resposta JSON devolvida ao frontend / sistema de CRM  |
| Mensagens "ALTA/BAIXA CHANCE"      | Ação de negócio acionada (e-mail, cupom, notificação) |

**Fluxo completo de deploy:**

```
[Backend E-commerce]
       │
       ▼
  JSON com dados do visitante (sessão em tempo real)
       │
       ▼
  [API Gateway] → [Validação/Transformação]
       │
       ▼
  [Modelo ML (pickle/serializado)] → predict_proba()
       │
       ▼
  [Regra de Negócio] → Se prob > 70% → dispara ação
       │
       ▼
  [CRM / Email Marketing / Push Notification]
```

### Sugestão de melhoria

Testar outras profundidades da árvore (`max_depth=2`, `max_depth=5`, `max_depth=None`) e comparar os resultados para observar o trade-off entre viés e variância (underfitting vs overfitting).
