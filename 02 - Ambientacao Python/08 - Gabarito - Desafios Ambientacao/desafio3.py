acessos = [
    ("/home", 200),
    ("/produtos", 200),
    ("/home", 200),
    ("/login", 403),
    ("/produtos", 200),
    ("/carrinho", 500),
    ("/home", 200)
]

contagem_urls = {}
total_erros = 0

for url, status in acessos:
    # Contagem de URLs
    if url in contagem_urls:
        contagem_urls[url] += 1
    else:
        contagem_urls[url] = 1

    # Contagem de erros
    if status >= 400:
        total_erros += 1

# URL mais acessada
url_mais_acessada = None
maior_valor = 0

for url, quantidade in contagem_urls.items():
    if quantidade > maior_valor:
        maior_valor = quantidade
        url_mais_acessada = url

urls_unicas = list(contagem_urls.keys())

print("Contagem por URL:", contagem_urls)
print("URL mais acessada:", url_mais_acessada)
print("Total de erros:", total_erros)
print("URLs únicas:", urls_unicas)