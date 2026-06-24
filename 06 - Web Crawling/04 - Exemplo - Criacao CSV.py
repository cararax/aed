import csv

# Exemplo de dados que os alunos podem ter coletado
dados_coletados = [
    {'categoria': 'produto', 'nome': 'Monitor 24', 'preco': 1450.90, 'info': 'Tela 4K, 60Hz'},
    {'categoria': 'noticia', 'nome': 'Workshop de Python', 'preco': 0.0, 'info': 'Local: Prédio 70'},
    {'categoria': 'produto', 'nome': 'Mouse Gamer', 'preco': 120.00, 'info': 'RGB, 7200 DPI'}
]

# Nome do arquivo de saída
arquivo_saida = 'dataset.csv'

# Definindo os cabeçalhos (colunas)
campos = ['categoria', 'nome', 'preco', 'info']

try:
    # newline='' evita linhas em branco extras no Windows
    # encoding='utf-8-sig' garante que o Excel abra os acentos corretamente
    with open(arquivo_saida, 'w', newline='', encoding='utf-8-sig') as csvfile:
        escritor = csv.DictWriter(csvfile, fieldnames=campos, delimiter=';')

        # Escreve o cabeçalho
        escritor.writeheader()

        # Escreve as linhas de dados
        escritor.writerows(dados_coletados)

    print(f"Sucesso! Arquivo '{arquivo_saida}' gerado corretamente.")

except Exception as e:
    print(f"Erro ao salvar o arquivo: {e}")