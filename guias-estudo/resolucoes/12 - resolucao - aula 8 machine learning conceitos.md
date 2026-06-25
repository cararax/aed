# Resumo — Aula 8: Machine Learning (Conceitos Fundamentais)

> **Fonte:** Slides da Aula 8 — Prof. Leandro O. Freitas
> Arquivo original: [`12 - Slides - Aula 8 - Machine Learning.odp`](../../08%20-%20Machine%20Learning/12%20-%20Slides%20-%20Aula%208%20-%20Machine%20Learning.odp)

---

## 📋 Sumário

- [O que é Machine Learning?](#o-que-é-machine-learning)
- [Machine Learning na Web](#machine-learning-na-web)
- [Dataset, Indivíduos, Features e Rótulos](#dataset-indivíduos-features-e-rótulos)
- [Como funciona um algoritmo de ML](#como-funciona-um-algoritmo-de-ml)
- [Treino e Teste](#treino-e-teste)
- [Aprendizagem Supervisionada](#aprendizagem-supervisionada)
- [Aprendizagem Não Supervisionada](#aprendizagem-não-supervisionada)
- [Aprendizagem por Reforço](#aprendizagem-por-reforço)
- [Regressão Linear](#regressão-linear)
- [Classificação](#classificação)
- [Clusterização](#clusterização)
- [Como escolher o modelo adequado?](#como-escolher-o-modelo-adequado)

---

## O que é Machine Learning?

> *"ML é um campo de estudo que dá ao computador a habilidade de aprender sem ser explicitamente programado."* — Samuel, A. 1959

### Programação Tradicional vs Aprendizado de Máquina

| Abordagem | Entrada | Processamento | Saída |
|-----------|---------|---------------|-------|
| **Programação Tradicional** | Dados + Regras | Computador aplica as regras | Respostas |
| **Aprendizado de Máquina** | Dados + Respostas (Exemplos) | Computador **aprende** as regras | Regras / Modelo |

O ML permite: **reconhecimento e análise de dados**, **identificação de padrões** e **tomada de decisões** baseada em dados.

---

## Machine Learning na Web

### Netflix (Recomendação)
- Analisa filmes assistidos, tempo de uso, avaliações, gêneros preferidos, usuários semelhantes
- **Técnicas:** classificação, clusterização, filtragem colaborativa

### Gmail (Classificação)
- Analisa conteúdo das mensagens (strings)
- **Técnica:** classificação (spam / não spam)

### Amazon (E-commerce)
- Analisa histórico de compras, produtos visualizados, carrinho abandonado, comportamento de clientes semelhantes
- **Técnica:** sistema de recomendação e previsão de interesse

```
Dados → ML → Decisões automáticas → Experiência personalizada
```

---

## Dataset, Indivíduos, Features e Rótulos

| Termo | Descrição | Analogia |
|-------|-----------|----------|
| **Dataset** | Conjunto de dados usado pelo algoritmo para aprender | A "tabela" completa |
| **Indivíduos (exemplos)** | Linhas do dataset (registros) | Cada aluno na planilha de notas |
| **Features (atributos)** | Colunas do dataset — características de cada indivíduo | Horas de estudo, faltas, exercícios |
| **Label (rótulo)** | Coluna "especial" que classifica os indivíduos (nem sempre presente) | Nota final, aprovado/reprovado |

### Exemplo ilustrativo

| Horas estudo | Faltas | Exercícios | **Nota (label)** |
|-------------|--------|------------|-----------------|
| 8 | 0 | 10 | 9 |
| 2 | 5 | 3 | 4 |

- **Features:** Horas estudo, Faltas, Exercícios
- **Label:** Nota (o que queremos prever)

---

## Como funciona um algoritmo de ML

```
Dataset (ex: 1000 imóveis conhecidos)
       ↓
Treinamento (algoritmo analisa os dados)
       ↓
Modelo (aprende os padrões)
       ↓
Previsão (estimar valor de um novo imóvel)
```

---

## Treino e Teste

O processo de treinamento de um modelo de ML passa por **duas etapas**:

### 1. Treino (Aprendizado)
O algoritmo analisa **parte dos dados** do dataset, identifica padrões nas características dos indivíduos e **aprende o comportamento** deles.

### 2. Teste (Avaliação)
Utiliza **outra parte dos dados** para **verificar se o que aprendeu está correto**.

> Geralmente divide-se o dataset em **80% para treino** e **20% para teste**.

---

## Aprendizagem Supervisionada

Trabalha com **dados rotulados** — para cada exemplo/amostra existe uma **saída (rótulo)** que os identifica.

### Características
- O aprendizado se dá pela **relação entre as features** (características) e a **saída esperada** (rótulo)
- **Objetivo:** a partir da análise de registros passados, **prever o comportamento** ou **tomar decisões** para situações futuras

### Exemplos
- Figuras de animais com seus nomes → identificar novas figuras
- Hábitos de navegação de usuários → sugerir dicas de pesquisa (viagens, música, comida)

### Exemplo prático: Recomendação de filmes

| Perfil | Gosta | Sugestão |
|--------|-------|----------|
| **A** | Fantasia | Harry Potter, Senhor dos Anéis, Crônicas de Nárnia |
| **B** | Ficção Científica | Star Wars, Star Trek |

> Quanto **maior o dataset** de entrada usado para treino, **mais preciso** será o resultado.

### Exemplo: Análise de Crédito

O resultado da aprendizagem supervisionada deve estar **relacionado aos rótulos** dos registros do dataset (ex: bom / mau pagador).

---

## Aprendizagem Não Supervisionada

Nesta abordagem **não usamos dados rotulados** — os registros do dataset **não possuem** um atributo que os identifica.

### Características
- **Objetivo:** agrupar elementos baseando-se nas suas **características e similaridades**, formando **clusters** (grupos)
- Não buscamos "respostas corretas" (rótulos), pois **não há**
- A acurácia é alcançada pelos **comportamentos semelhantes** entre indivíduos do mesmo grupo

### Exemplos
- Conjunto de imagens de animais → separar felinos de caninos
- Itens comprados online → identificar hábitos de compra e agrupar por localização geográfica ou idade

### Exemplo prático: Campanhas de Supermercado

```
Cenário: Uma rede de supermercados quer maximizar vendas
         criando campanhas específicas para cada grupo de clientes.

Após agrupar clientes por hábitos de compra e métodos de pagamento:

  ┌──────────────────────────────┐
  │ Idosos                       │ → Descontos seg/ter
  │ Pagamentos com cartão        │ → Promoções sextas
  │ Compras de produtos de bebê  │ → Ofertas sábados
  │ Compras abaixo de R$ 50,00   │ → Cupons de desconto
  └──────────────────────────────┘
```

---

## Aprendizagem por Reforço

Utiliza a técnica de **recompensa e punição** para o treinamento:

- **Agente de IA** realiza ações em um ambiente e **aprende com experiências**
- **Recebe recompensa** ao realizar ação correta
- **Recebe punição** ao realizar ação incorreta
- **Objetivo:** maximizar as recompensas
- **Constrói seu dataset** durante o processo de análise dos estados do ambiente

### Analogia

| Situação | Descrição |
|----------|-----------|
| **Ser humano** | Uma criança aprende coisas por experiências no dia-a-dia |
| **Jogo** | A cada ação correta, o jogador avança e ganha pontos; a cada erro, é punido |

### Exemplos reais
- Ensinar uma máquina a **jogar xadrez** — atribuindo pontuações a cada movimento
- **Carros autônomos** (*driveless cars*) — aprendem a dirigir por tentativa e erro

---

## Regressão Linear

> **Regressão Linear** é um método de ML usado para **prever um valor numérico**.

### Como funciona
1. Encontra a **relação mais simples** entre duas coisas:
   - A **informação que você tem** (ex: horas de estudo)
   - A **informação que quer prever** (ex: nota final)
2. O algoritmo "aprende" analisando **vários exemplos passados** e **desenha a linha de tendência** que melhor representa essa relação
3. Quando um novo dado chega, usa essa linha para **prever o resultado**

### Exemplo: Previsão de Preços de Imóveis

| Imóvel | Tamanho | Preço (em Mil R$) |
|--------|---------|-------------------|
| A | 50 m² | 200 |
| B | 70 m² | 280 |
| C | 100 m² | 410 |
| D | 120 m² | 470 |

> O modelo aprende: **a cada 1 m² a mais, o preço tende a subir ~R$ 3.900**

**Pergunta:** Qual o valor de um imóvel de **90 m²**?
**Resposta:** A regressão linear estima cerca de **R$ 360 mil**.

```
Dados conhecidos → Treinar modelo → Modelo aprende padrões → Estimar novo valor
```

---

## Classificação

Conjunto de algoritmos para **classificação de dados categorizados**.

### Características
- A partir de perguntas com **respostas pré-definidas** (sim/não, macho/fêmea, sol/chuva/nublado)
- As perguntas são aplicadas aos **atributos** (features) dos registros
- **Algoritmos comuns:** Árvores de Decisão, Random Forests, Support Vector Machine (SVM)

### Exemplo: Árvore de Decisão

Utiliza análise de métricas estatísticas (**entropia, gini impurity, information gain**) para encontrar a(s) pergunta(s) mais adequadas durante o processo de classificação.

```
                 ┌──────────────────┐
                 │   Idade > 30?    │
                 └────────┬─────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
   ┌────────────────┐          ┌────────────────┐
   │  Renda > 5K?   │          │  Renda > 8K?   │
   └───────┬────────┘          └───────┬────────┘
           │                           │
      ┌────┴────┐                 ┌────┴────┐
      ▼         ▼                 ▼         ▼
   ┌─────┐   ┌─────┐          ┌─────┐   ┌─────┐
   │ Mau │   │ Bom │          │ Mau │   │ Bom │
   └─────┘   └─────┘          └─────┘   └─────┘
```

---

## Clusterização

Processo de **agrupar indivíduos de acordo com suas similaridades**.

### Características
- A definição do cluster se baseia na **análise das diferenças** entre as características dos indivíduos
- A criação dos clusters é feita a partir da **busca por padrões em dados não rotulados** (forma, tamanho, comportamento)
- A quantidade de clusters necessária deve ser **definida de acordo com as características** dos dados

### Tipos de Clusterização

| Tipo | Descrição |
|------|-----------|
| **Hard Clustering** | Indivíduos pertencem a **apenas um** grupo |
| **Soft Clustering** | Indivíduos podem pertencer a **um ou mais** grupos |

### Algoritmo K-Means
- Dataset é dividido em **k grupos** (total de clusters)
- Define-se o **centro de cada cluster (centróide)**
- A distância dos centróides para os indivíduos do cluster deve ser **mínima** quando comparada a outros centróides

### Exemplos práticos
- Seções de produtos em supermercados ou lojas
- Agrupamento de documentos de acordo com tópicos
- Segmentação de imagens, detecção de anomalias
- Sistemas de recomendação (e-commerce, streaming)

### Exemplo: Segmentação de Clientes

```
                 ┌─────────────────────────────────────┐
Tentando definir │   Base de Clientes (idade x renda)  │
público alvo:    └─────────────────────────────────────┘
                              │
                              ▼
                 ┌─────────────────────────────────────┐
Usando           │   Clusterização aplicada aos dados  │
clusterização:   │    ┌─────┐ ┌─────┐ ┌─────┐         │
                 │    │  A  │ │  B  │ │  C  │         │
                 │    └─────┘ └─────┘ └─────┘         │
                 └─────────────────────────────────────┘
                              │
                              ▼
                 ┌─────────────────────────────────────┐
Vendendo para o  │   Campanha direcionada por cluster  │
público alvo:    └─────────────────────────────────────┘
```

---

## Como escolher o modelo adequado?

| Problema | Técnica Recomendada |
|----------|-------------------|
| Prever **preço de imóvel** (valor numérico) | **Regressão** |
| **Aprovar crédito** (sim/não) | **Classificação** |
| **Agrupar clientes** (descobrir grupos) | **Clusterização** |
| Treinar **robô para jogar** (aprender por tentativa) | **Reforço** |

---

## Mapa Mental — Tipos de Aprendizado

```
                    ┌──────────────────────────┐
                    │   APRENDIZADO DE MÁQUINA  │
                    └──────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  ┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
  │ SUPERVISIONADO│   │ NÃO SUPERVISIONADO│   │   REFORÇO   │
  └─────────────┘    └─────────────────┘    └──────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │ • Dados com  │    │ • Dados sem  │    │ • Agente     │
  │   rótulo     │    │   rótulo     │    │   aprende    │
  │ • Prever     │    │ • Agrupar    │    │   por        │
  │   classes/   │    │   por        │    │   tentativa  │
  │   valores    │    │   similari-  │    │ • Recompensa │
  │              │    │   dade       │    │   e punição  │
  └──────────────┘    └──────────────┘    └──────────────┘
         │                    │
         ▼                    ▼
  ┌──────────────┐    ┌──────────────┐
  │ Regressão    │    │ Clusterização│
  │ Classificação│    │ (K-Means...)  │
  │ (Árvore      │    └──────────────┘
  │  Decisão,    │
  │  SVM, RF...) │
  └──────────────┘
```

---

> 📎 **Arquivo original:** [`08 - Machine Learning/12 - Slides - Aula 8 - Machine Learning.odp`](../../08%20-%20Machine%20Learning/12%20-%20Slides%20-%20Aula%208%20-%20Machine%20Learning.odp)
> 👨‍🏫 **Professor:** Leandro O. Freitas — leandro@politecnico.ufsm.br
