status_codes = [200, 404, 500, 301, 403, 200, 502, 201]

def classificar_status(code):
    if 200 <= code <= 299:
        return "Sucesso"
    elif 300 <= code <= 399:
        return "Redirecionamento"
    elif 400 <= code <= 499:
        return "Erro do Cliente"
    elif 500 <= code <= 599:
        return "Erro do Servidor"
    else:
        return "Desconhecido"

contagem = {
    "Sucesso": 0,
    "Redirecionamento": 0,
    "Erro do Cliente": 0,
    "Erro do Servidor": 0,
    "Desconhecido": 0
}

for code in status_codes:
    categoria = classificar_status(code)
    contagem[categoria] += 1

print("Relatório:")
for categoria, quantidade in contagem.items():
    print(f"{categoria}: {quantidade}")