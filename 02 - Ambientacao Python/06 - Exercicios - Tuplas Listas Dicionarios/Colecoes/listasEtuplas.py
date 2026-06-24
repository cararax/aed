"""
Manipulação de uma Lista de Compras:
Crie uma lista chamada compras com os seguintes itens:
"leite", "pão", "ovos". Depois:
- Adicione "queijo" ao final da lista;
- Remova "pão" da lista;
- Substitua o item "leite" por "iogurte";
- Imprima a lista final.
"""

def exercicio1():
    compras = ["leite", "pão", "ovos"]
    compras.append("queijo")
    print(compras)
    compras.remove("pão")
    print(compras)
    compras.insert(0, "iogurte")
    print(compras)


"""
2. Análise de Tupla de Coordenadas:
 Considere a seguinte tupla de coordenadas: ponto_cartesiano = (10, 20). 
 Depois:
    Acesse e imprima o valor da coordenada X (o primeiro elemento);
    Tente modificar o valor da coordenada Y para 25. O que acontece? 
    Explique o motivo do erro (se houver).
"""
def exercicio2():
    ponto_cartesiano = (10, 20)
    print(ponto_cartesiano[0])
    ponto_cartesiano[1] = 30
    print(ponto_cartesiano)

"""
3. Conversão e Junção de Dados:
Você tem uma lista de números inteiros numeros_pares = [2, 4, 6, 8] 
e uma tupla de números ímpares numeros_impares = (1, 3, 5, 7). Então:
    Converta a tupla numeros_impares em uma lista (pesquisar sobre);
    Combine as duas listas em uma única lista chamada numeros_completos;
    Ordene a lista numeros_completos em ordem crescente e a imprima.
"""
def exercicio3():
    numeros_pares = [2, 4, 6, 8]
    numeros_impares = (1, 3, 5, 7)
    lista_impares = list(numeros_impares)
    numeros_pares = numeros_pares + lista_impares
    print(numeros_pares)
    numeros_pares.sort()
    print(numeros_pares)

"""
4. Cálculo e Contagem de Elementos:
Dada a lista temperaturas_cidade = [25.5, 27.0, 26.5, 25.5, 28.1, 25.5], 
faça o solicitado:
    Calcule e imprima a temperatura média;
    Conte quantas vezes a temperatura 25.5 aparece 
    na lista e imprima o resultado.
"""
def exercicio4():
    temperaturas_cidade = [25.5, 27.0, 26.5, 25.5, 28.1, 25.5]
    media = (sum(temperaturas_cidade)) / 6
    print(f"Média de temperaturas: {media:.2f}")
"""
5. Aninhamento de Estruturas:
Crie uma lista chamada catalogo_produtos. 
Cada elemento desta lista deve ser uma tupla contendo o nome do produto
 e seu preço. Adicione três produtos de sua escolha. Depois:
    Imprima o nome e o preço do segundo produto no catálogo;
    Adicione um novo produto ("computador", 5000.00) ao catálogo;
    Percorra a lista e imprima cada produto no formato: 
    "Produto: [nome] - Preço: R$[preço]".
"""

def exercicio5():
    catalogo_produtos = []
    catalogo_produtos = [('meia',10.00), ('camiseta', 55.90)]
    print(catalogo_produtos[1])
    catalogo_produtos.append(('computador', 5000.00))
    print(catalogo_produtos)
    for nome, preco in catalogo_produtos:
       print(f"Produto [{nome}] - Preço: R$[{preco}]")

