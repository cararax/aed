# Resolução — Exercícios: Tuplas, Listas e Dicionários

---

## Sumário

- [Exercício 1 — Lista de compras (append / remove / insert)](#exercicio-1)
- [Exercício 2 — Imutabilidade de tuplas](#exercicio-2)
- [Exercício 3 — Conversão tupla → lista, junção e sort](#exercicio-3)
- [Exercício 4 — Média de temperaturas com lista](#exercicio-4)
- [Exercício 5 — Catálogo de produtos (lista de tuplas)](#exercicio-5)
- [Exercício 6 — Dicionário de dados pessoais](#exercicio-6)
- [Exercício 7 — Agenda de contatos com dicionário](#exercicio-7)

---

## Exercício 1

**Enunciado:**  
Crie uma lista chamada `compras` com `"leite"`, `"pão"`, `"ovos"`.
Depois:
1. Adicione `"queijo"` ao final;
2. Remova `"pão"`;
3. Substitua `"leite"` por `"iogurte"` (inserindo no índice 0);
4. Imprima a lista final.

```python
def exercicio1():
    """
    Demonstra operações básicas em listas:
    append(), remove() e insert().
    """

    # Criação de lista literal — colchetes [] delimitam os elementos.
    compras = ["leite", "pão", "ovos"]

    # append(item) — adiciona UM elemento ao FINAL da lista.
    # A lista passa a ter 4 elementos.
    compras.append("queijo")
    print(compras)  # ['leite', 'pão', 'ovos', 'queijo']

    # remove(item) — remove a PRIMEIRA ocorrência do item.
    # Se o item não existir, lança ValueError.
    # A lista passa a ter 3 elementos.
    compras.remove("pão")
    print(compras)  # ['leite', 'ovos', 'queijo']

    # insert(posição, item) — insere o item na posição indicada,
    # deslocando os elementos seguintes para a direita.
    # Aqui inserimos "iogurte" no índice 0 (início da lista).
    # A lista passa a ter 4 elementos de novo.
    compras.insert(0, "iogurte")
    print(compras)  # ['iogurte', 'leite', 'ovos', 'queijo']
```

---

## Exercício 2

**Enunciado:**  
Considere a tupla `ponto_cartesiano = (10, 20)`.
1. Acesse e imprima o valor de X;
2. Tente modificar Y para 25 — explique o erro.

```python
def exercicio2():
    """
    Demonstra a IMUTABILIDADE das tuplas.
    Uma tupla, depois de criada, NÃO pode ter seus elementos
    alterados, adicionados ou removidos.
    """

    # Tupla — parênteses () delimitam, mas não são obrigatórios.
    # A diferença fundamental para listas: tupla é IMUTÁVEL.
    ponto_cartesiano = (10, 20)

    # Acesso por índice — funciona igual à lista.
    # Índices começam em 0.
    print(ponto_cartesiano[0])  # Exibe 10 (coordenada X)

    # Tentativa de modificação — isso vai gerar um erro!
    # ----------------------------------------------------
    # O Python lança TypeError: 'tuple' object does not support
    # item assignment. Tuplas não permitem atribuição em índices
    # porque foram projetadas para serem imutáveis.
    #
    # Isso é útil quando queremos GARANTIR que os dados não
    # serão alterados acidentalmente (ex: coordenadas fixas,
    # dias da semana, etc.).
    ponto_cartesiano[1] = 30  # ← TypeError!

    # O código abaixo NUNCA executa se a linha acima estourar erro.
    print(ponto_cartesiano)
```

---

## Exercício 3

**Enunciado:**  
Você tem `numeros_pares = [2, 4, 6, 8]` (lista) e
`numeros_impares = (1, 3, 5, 7)` (tupla).  
1. Converta a tupla em lista;  
2. Combine as duas listas;  
3. Ordene em ordem crescente e imprima.

```python
def exercicio3():
    """
    Conversão de tupla para lista e combinação com sort().
    """

    # Lista de pares
    numeros_pares = [2, 4, 6, 8]

    # Tupla de ímpares
    numeros_impares = (1, 3, 5, 7)

    # list(tupla) — converte a tupla em uma NOVA lista.
    # A tupla original permanece inalterada.
    lista_impares = list(numeros_impares)  # [1, 3, 5, 7]

    # Concatenação de listas com o operador +
    # Cria uma NOVA lista unindo os elementos das duas.
    # numeros_pares = [2, 4, 6, 8] + [1, 3, 5, 7]
    numeros_pares = numeros_pares + lista_impares
    print(numeros_pares)  # [2, 4, 6, 8, 1, 3, 5, 7] (ainda desordenado)

    # sort() — ordena a lista INPLACE (modifica a própria lista).
    # Ordem crescente (padrão) → menor para maior.
    # Se quiséssemos decrescente: sort(reverse=True).
    numeros_pares.sort()
    print(numeros_pares)  # [1, 2, 3, 4, 5, 6, 7, 8]
```

---

## Exercício 4

**Enunciado:**  
Dada `temperaturas_cidade = [25.5, 27.0, 26.5, 25.5, 28.1, 25.5]`:
1. Calcule e imprima a temperatura média;
2. Conte quantas vezes 25.5 aparece.

```python
def exercicio4():
    """
    Cálculo de média aritmética e contagem de ocorrências.
    """

    temperaturas_cidade = [25.5, 27.0, 26.5, 25.5, 28.1, 25.5]

    # sum(lista) — função embutida que soma todos os elementos.
    # Equivalente a fazer um for acumulando cada valor.
    # Resultado: 25.5 + 27.0 + 26.5 + 25.5 + 28.1 + 25.5 = 158.1

    # Dividimos pela quantidade de elementos (6) para obter a média.
    # Usamos :.2f na f-string para exibir com 2 casas decimais.
    media = sum(temperaturas_cidade) / 6
    print(f"Média de temperaturas: {media:.2f}")

    # count(valor) — método da lista que conta ocorrências.
    # Percorre a lista internamente e retorna quantas vezes
    # o valor aparece.
    # 25.5 aparece 3 vezes (índices 0, 3, 5).
    print(f"25.5 aparece {temperaturas_cidade.count(25.5)} vezes")
```

---

## Exercício 5

**Enunciado:**  
Crie uma lista `catalogo_produtos` onde cada elemento é uma tupla
`(nome, preço)`. Adicione 3 produtos. Depois:
1. Imprima nome e preço do **segundo** produto;
2. Adicione `("computador", 5000.00)`;
3. Percorra a lista e exiba `"Produto: [nome] - Preço: R$[preço]"`.

```python
def exercicio5():
    """
    Lista de tuplas — estrutura aninhada.
    Cada tupla representa um produto (nome, preço).
    """

    # Lista vazia (vai ser preenchida depois)
    catalogo_produtos = []

    # Atribuindo diretamente uma lista com 2 tuplas
    catalogo_produtos = [('meia', 10.00), ('camiseta', 55.90)]

    # Acessando o segundo elemento (índice 1)
    # catalogo_produtos[1] → ('camiseta', 55.90)
    print(catalogo_produtos[1])

    # append(tupla) — adiciona uma nova tupla ao catálogo
    catalogo_produtos.append(('computador', 5000.00))
    print(catalogo_produtos)

    # Desempacotamento de tupla no for
    # ----------------------------------
    # for nome, preco in catalogo_produtos:
    # A cada iteração o Python "desempacota" a tupla atual
    # em duas variáveis: nome e preco.
    # É equivalente a:
    #   for produto in catalogo_produtos:
    #       nome, preco = produto
    for nome, preco in catalogo_produtos:
        print(f"Produto [{nome}] - Preço: R$[{preco}]")
```

---

## Exercício 6

**Enunciado:**  
Crie um dicionário e armazene nele os seus dados:
`nome`, `idade`, `telefone`, `endereço`.
Imprima tudo no formato `chave: valor`.

```python
def dict1():
    """
    Dicionário — estrutura chave → valor.
    As chaves são únicas e imutáveis (strings, números, tuplas).
    """

    # Dicionário vazio — chaves {}.
    dict = {}

    # Atribuição por chave — se a chave não existe, é criada.
    # Se já existe, o valor é sobrescrito.
    dict['nome'] = 'joao'
    dict['idade'] = 50
    dict['telefone'] = '991 991 991'
    dict['end'] = 'Av. Roraima, 1000'

    # dict.items() — retorna uma visão dos pares (chave, valor).
    # É um iterável de tuplas: ('nome', 'joao'), ('idade', 50), ...
    # Desempacotamos cada tupla em k (chave) e v (valor).
    for k, v in dict.items():
        print(f"{k}: {v}")
```

---

## Exercício 7

**Enunciado:**  
Crie um programa que, usando dicionário, crie uma **agenda** de
tamanho fornecido pelo usuário. Leia os dados de todos os contatos
e no final imprima todos.

```python
def dict2():
    """
    Agenda de contatos com dicionário aninhado.
    Cada contato é um dicionário dentro de outro dicionário.
    """

    # Dicionário principal — cada chave é o nome do contato,
    # cada valor é um sub-dicionário com os detalhes.
    agenda = {}

    # int(input(...)) — lê a quantidade de contatos.
    n = int(input("Quantos contatos? "))

    # Loop para ler os dados de cada contato
    for i in range(n):
        print(f"\n--- Contato {i + 1} ---")

        # Lê o nome (será a chave no dicionário principal)
        nome = input("Nome: ")

        # Lê os demais campos
        telefone = input("Telefone: ")
        email = input("E-mail: ")

        # Aninhamento de dicionários
        # ----------------------------
        # agenda[nome] = { 'telefone': ..., 'email': ... }
        # O valor associado à chave 'nome' é OUTRO dicionário.
        agenda[nome] = {
            'telefone': telefone,
            'email': email
        }

    # Exibindo todos os contatos
    print("\n=== AGENDA ===")

    # Percorrendo o dicionário principal
    for nome, dados in agenda.items():
        # nome → chave (string)
        # dados → sub-dicionário com 'telefone' e 'email'
        print(f"Nome: {nome}")
        print(f"  Telefone: {dados['telefone']}")
        print(f"  E-mail: {dados['email']}")
        print("-" * 30)
```
