try:
    url = input("Digite a URL: ")
    tentativas = int(input("Digite o número de tentativas: "))

    if tentativas <= 0:
        raise ValueError("Número de tentativas deve ser maior que zero.")

    for i in range(tentativas):
        print(f"Tentativa {i + 1} de acessar {url}")

        # Simulação de erro proposital
        resultado = 10 / (tentativas - i - 1)

except ValueError as e:
    print("Erro de valor:", e)

except ZeroDivisionError:
    print("Erro: divisão por zero ocorreu durante simulação.")

except Exception as e:
    print("Erro inesperado:", e)

else:
    print("Execução concluída sem erros.")

finally:
    print("Encerrando programa.")