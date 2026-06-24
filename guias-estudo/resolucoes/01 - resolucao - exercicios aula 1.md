# Resolução — Exercícios Aula 1 (Ambientação Python)

---

## Sumário

- [Exercício 1 — Cálculo de desconto / juros conforme forma de pagamento](#exercicio-1)
- [Exercício 2 — Repetir leitura até que primeiro valor seja menor que o segundo](#exercicio-2)
- [Exercício 3 — Só aceitar valores maiores que o anterior](#exercicio-3)
- [Exercício 4 — Número perfeito](#exercicio-4)
- [Exercício 5 — Duração de jogo que pode virar o dia](#exercicio-5)

---

## Exercício 1

**Enunciado:**  
Desenvolva um algoritmo que leia o valor a ser pago por um produto, considerando
o preço normal de etiqueta e a escolha da condição de pagamento.

| Código | Condição |
|--------|----------|
| `dinheiro` ou `cheque` | 10 % de desconto |
| `credito` | 15 % de desconto |
| parcelado em 2× | acréscimo de 10 % |

```python
def exercicio1():
    """
    Lê o valor do produto e a forma de pagamento, aplica a regra
    correspondente e exibe o valor final.
    """

    # float(input(...)) — convertendo para float
    # --------------------------------------------
    # input() SEMPRE retorna uma string (texto) digitado pelo usuário.
    # Para fazer contas precisamos de um número. float() transforma
    # a string em um número decimal (ponto flutuante).
    # Ex: "49.90" vira 49.9 (float).
    valor = float(input("Digite o valor a ser pago: "))

    # A forma de pagamento continua sendo uma string — não faremos
    # contas com ela, só comparações.
    pagamento = input("Digite a forma de pagamento: ")

    # if / elif / else — fluxo condicional
    # ------------------------------------
    # O Python testa CADA condição de cima para baixo.
    #   - A primeira que for True executa seu bloco e PULA as demais.
    #   - Se nenhuma for True, o else (opcional) executa.
    #
    # Importante: usamos "or" para juntar duas condições —
    # se pagamento for "dinheiro" OU "cheque" o if entra.

    if pagamento == "dinheiro" or pagamento == "cheque":
        # 10 % de desconto → multiplica por 0.9 (100% - 10% = 90%)
        print("Valor a ser pago: %.2f" % (valor * 0.9))

    elif pagamento == "credito":
        # 15 % de desconto → multiplica por 0.85 (100% - 15% = 85%)
        print("Valor a ser pago: %.2f" % (valor * 0.85))

    else:
        # Qualquer outra forma (parcelado, etc.) → acréscimo de 10 %
        # Multiplica por 1.1 (100% + 10% = 110%)
        print("Valor a ser pago: %.2f" % (valor * 1.1))
```

---

## Exercício 2

**Enunciado:**  
Faça um programa para ler diversos valores para duas variáveis inteiras
até que a primeira seja **menor** que a segunda.

```python
def exercicio2():
    """
    Lê dois inteiros e continua lendo novos pares até que
    x (primeiro) seja MENOR que y (segundo).
    """

    # int(input(...)) — convertendo para inteiro
    # --------------------------------------------
    # input() retorna string; int() converte para número inteiro.
    # Se o usuário digitar "10", vira o inteiro 10.
    # Se digitar "abc", int() lança ValueError (veremos exceções depois).

    x = int(input("digite o primeiro valor: "))
    y = int(input("digite o segundo valor: "))

    # while — loop de repetição
    # --------------------------
    # Enquanto a condição for True, o bloco repete.
    # Aqui: enquanto x >= y, pedimos novos valores.
    # A hora que x < y, o loop termina e vamos pro print.

    while x >= y:
        x = int(input("digite o primeiro valor: "))
        y = int(input("digite o segundo valor: "))

    # f-string — formatação moderna
    # ------------------------------
    # f"..." permite colocar expressões dentro de {}.
    # Equivalente a: print("Valor de x: {}".format(x))

    print(f"Valor de x: {x}")
    print(f"Valor de y: {y}")
```

---

## Exercício 3

**Enunciado:**  
Desenvolva um algoritmo que **somente** permita a leitura de valores
**maiores** que os lidos anteriormente. Defina uma condição de parada.

```python
def exercicio3():
    """
    Lê valores e só aceita o próximo se for MAIOR que o anterior.
    Quando o usuário digitar um valor menor ou igual ao anterior,
    o programa para.
    """

    # Lê o primeiro valor e armazena em x (referência).
    x = int(input("Digite o valor: "))

    # flag — variável de controle
    # ----------------------------
    # Uma flag (bandeira) é uma variável booleana que indica
    # se uma determinada condição já ocorreu.
    # Começa como False (ninguém digitou algo errado ainda).
    flag = False

    # while not flag — repete ENQUANTO flag for False
    # Quando flag virar True, o loop termina.
    while not flag:

        y = int(input("Digite o valor: "))

        # Se o NOVO valor (y) for MENOR que o anterior (x),
        # violamos a regra → flag = True → para o loop.
        if x > y:
            flag = True     # Condição de parada

        else:
            # Se y >= x, o valor é aceito.
            # Atualizamos x para o novo valor e continuamos.
            x = y

    # Exibe o par que violou a regra.
    print(f"Valor de x: {x}")
    print(f"Valor de y: {y}")
```

---

## Exercício 4

**Enunciado:**  
Faça uma função que verifique se um valor é **perfeito** ou não.
Um valor é perfeito quando é igual à soma dos seus divisores,
excluindo ele próprio (ex: 6 = 1 + 2 + 3). A função deve retornar
1 (perfeito) ou 0 (não perfeito).

```python
def exercicio4():
    """
    Verifica se o número digitado é perfeito.
    Número perfeito: a soma de seus divisores (excluindo ele mesmo)
    é igual a ele próprio.
    Exemplos: 6, 28, 496, 8128.
    """

    x = int(input("Digite o valor: "))
    soma = 0

    # range(1, x) — o que ele faz?
    # ------------------------------
    # range(início, fim) gera uma sequência de números INTEIROS
    # de início até fim-1 (o fim NÃO é incluído).
    # Ex: range(1, 7) → 1, 2, 3, 4, 5, 6.
    #
    # Aqui usamos range(1, x) para percorrer todos os candidatos
    # a divisor de x, MENOS o próprio x.
    #
    # Por que começa em 1? Porque 1 divide qualquer inteiro.
    # Por que termina em x-1? Porque não queremos incluir x
    # (a definição diz "excetuando ele próprio").

    for i in range(1, x):

        # Operador % — resto da divisão
        # ------------------------------
        # x % i calcula o RESTO de x dividido por i.
        # Se x % i == 0, então i divide x exatamente → é divisor.
        if (x % i == 0):
            soma += i       # Acumula o divisor na variável soma

    # Se a soma dos divisores for igual ao número, é perfeito.
    if soma == x:
        print("Valor perfeito")
    else:
        print("Não é perfeito")
```

---

## Exercício 5

**Enunciado:**  
Desenvolva um algoritmo com uma função que recebe por parâmetro
a hora de início e término de um jogo, ambas subdivididas em
2 valores distintos: **horas** e **minutos**. A função deve apresentar
a duração do jogo em horas e minutos, considerando que:

- O tempo máximo de duração de um jogo é de 24 horas;
- O jogo pode começar em um dia e terminar no outro.

```python
def exercicio5():
    """
    Calcula a duração de um jogo que pode começar num dia
    e terminar no dia seguinte (madrugada).
    """

    # Valores de exemplo: início 22:30, fim 01:15
    hora_inicio = 22
    minuto_inicio = 30
    hora_fim = 1
    minuto_fim = 15

    # Convertendo tudo para minutos — por que?
    # ------------------------------------------
    # Trabalhar com horas e minutos separados exige cuidado
    # com "empresta 1 hora = 60 minutos" nos cálculos.
    # A estratégia mais simples: converter TUDO para minutos
    # e depois converter o resultado de volta para horas+minutos.

    # início_total_minutos = 22 * 60 + 30 = 1320 + 30 = 1350
    inicio_total_minutos = hora_inicio * 60 + minuto_inicio

    # fim_total_minutos = 1 * 60 + 15 = 60 + 15 = 75
    fim_total_minutos = hora_fim * 60 + minuto_fim

    # Como detectar que virou o dia?
    # --------------------------------
    # Se o horário de fim (em minutos) for MENOR que o de início,
    # significa que o jogo passou da meia-noite.
    #   Ex: 75 (01:15) < 1350 (22:30) → sim, virou o dia.
    #
    # Nesse caso, adicionamos 24 horas (1440 minutos) ao horário
    # de fim para poder fazer a subtração corretamente.
    #
    #   Novo fim = 75 + 1440 = 1515
    #   Duração  = 1515 - 1350 = 165 minutos

    if fim_total_minutos < inicio_total_minutos:
        fim_total_minutos += 24 * 60   # 24h = 1440 minutos

    # Diferença em minutos
    duracao_total_minutos = fim_total_minutos - inicio_total_minutos

    # Convertendo minutos de volta para horas e minutos
    # --------------------------------------------------
    # // → divisão INTEIRA (descarta a parte decimal)
    #      Ex: 165 // 60 = 2 (horas)
    # %  → resto da divisão
    #      Ex: 165 % 60 = 45 (minutos)

    duracao_horas = duracao_total_minutos // 60
    duracao_minutos = duracao_total_minutos % 60

    print(f'Duração do jogo: {duracao_horas} horas e {duracao_minutos} minutos')
    # Exibe: "Duração do jogo: 2 horas e 45 minutos"
```
