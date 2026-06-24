log = '192.168.0.10 - - [03/Mar/2026:10:15:32] "GET /produtos?id=10 HTTP/1.1" 200 532'

# Separando por espaços
partes = log.split()

ip = partes[0]

# A requisição está entre aspas
indice_inicio = log.find('"')
indice_fim = log.find('"', indice_inicio + 1)

requisicao = log[indice_inicio + 1:indice_fim]
metodo, url, protocolo = requisicao.split()

status = partes[-2]
tamanho = partes[-1]

print(f"IP: {ip}")
print(f"Método: {metodo}")
print(f"URL: {url}")
print(f"Status: {status}")
print(f"Tamanho da resposta: {tamanho} bytes")