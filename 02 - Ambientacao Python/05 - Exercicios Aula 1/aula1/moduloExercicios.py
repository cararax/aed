from datetime import datetime

"""
Desenvolva um algoritmo que leia o valor a ser pago por um produto,
considerando o preço normal de etiqueta e a escolha da condição
de pagamento. Para realizar o cálculo, utilize os códigos a
seguir referentes à condição de pagamento escolhida pelo cliente.

Código Condição de pagamento;
À vista em dinheiro ou cheque, recebe 10% de desconto.
À vista no cartão de crédito, recebe 15% de desconto.
Em duas vezes, preço normal de etiqueta mais juros de 10%.
"""

def exercicio1():
    valor = float(input("Digite o valor a ser pago: "))
    pagamento = input("Digite a forma de pagamento: ")

    if pagamento == "dinheiro" or pagamento == "cheque":
        print("Valor a ser pago: %.2f" % (valor * 0.9))
    elif pagamento == "credito":
        print("Valor a ser pago: %.2f" % (valor * 0.85))
    else:
        print("Valor a ser pago: %.2f" % (valor * 1.1))


def exercicio2():
    """
    Faça um programa para ler diversos valores para duas variáveis
    inteiras até que a primeira seja menor que a segunda.
    """
    x = int(input("digite o primeiro valor: "))
    y = int(input("digite o segundo valor: "))

    while x >= y:
        x = int(input("digite o primeiro valor: "))
        y = int(input("digite o segundo valor: "))

    print(f"Valor de x: {x}")
    print(f"Valor de y: {y}")


def exercicio3():
    """
    Desenvolva um algoritmo que somente permita a leitura de valores maiores
    que os lidos anteriormente.
    Você deve definir uma condição de parada para o programa.
    """
    x = int(input("Digite o valor: "))
    flag = False
    while not flag:
        y = int(input("Digite o valor: "))
        if x > y:
            flag = True
        else:
            x = y

    print(f"Valor de x: {x}")
    print(f"Valor de y: {y}")

def exercicio4():
    """
    Faça uma função que verifique se um valor é perfeito ou não.
    Um valor é dito perfeito quando ele é igual a soma dos seus
     divisores excetuando ele próprio.
     (Ex: 6 é perfeito, 6 = 1 + 2 + 3, que são seus divisores).
     A função deve retornar 1, caso o número seja perfeito ou 0,
     caso não seja.

    """
    x = int(input("Digite o valor: "))
    soma = 0

    for i in range(1, x):
        if(x % i == 0):
            soma += i

    if soma == x:
        print("Valor perfeito")
    else:
        print("Não é perfeito")

def exercicio5():
    """
    RESOLVIDO APENAS COM DATETIME

    Desenvolva um algoritmo com uma função que recebe por parâmetro
    a hora de início e término de um jogo, ambas subdivididas em
    2 valores distintos: horas e minutos. A função deve apresentar a
    duração do jogo em horas e minutos, considerando que o tempo
    máximo de duração de um jogo é de 24 horas e que o jogo pode
    começar em um dia e terminar no outro.
    """
    hora_inicio = 22
    minuto_inicio = 30
    hora_fim = 1
    minuto_fim = 15

    # Converte horas e minutos para minutos totais desde o começo do dia
    inicio_total_minutos = hora_inicio * 60 + minuto_inicio
    fim_total_minutos = hora_fim * 60 + minuto_fim

    # Se o fim for antes do início, então o jogo se estendeu para o dia seguinte
    if fim_total_minutos < inicio_total_minutos:
        fim_total_minutos += 24 * 60  # Adiciona 24 horas em minutos

    duracao_total_minutos = fim_total_minutos - inicio_total_minutos

    # Convertendo a diferença de minutos para horas e minutos
    duracao_horas = duracao_total_minutos // 60
    duracao_minutos = duracao_total_minutos % 60

    print(f'Duração do jogo: {duracao_horas} horas e {duracao_minutos} minutos')