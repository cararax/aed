import pandas
from matplotlib import pyplot
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

"""
Utilize o arquivo disponibilizado pelo professor: Exercicio-custering-usuarios-site.csv
Parte 1 – Explorando os Dados:
Carregue o arquivo CSV utilizando a biblioteca Pandas;
Exiba as cinco primeiras linhas do conjunto de dados;
Informe a quantidade total de registros existentes.
"""

print("iniciando processo")
dataframe = pandas.read_csv("../01 - Dados - Clustering.csv")
print(dataframe.shape)
print(dataframe.head(5))
print(dataframe.count())
"""
Parte 2 – Visualização dos Dados:
Crie um gráfico de dispersão utilizando:
Eixo X: horas_semana;
Eixo Y: dias_acesso_mes.
Observe o gráfico gerado e responda:
Quantos grupos parecem existir visualmente nos dados?

Aparentemente existem 3. Inicio meio e fim.
"""
plot = pyplot
plot.scatter(dataframe["horas_semana"], dataframe["dias_acesso_mes"])
plot.xlabel("horas_semana")
plot.ylabel("dias_acesso_mes")
plot.show()

"""
Parte 3 – Aplicando o Algoritmo K-Means:
Utilize o algoritmo K-Means com: n_clusters = 4;
Execute o treinamento do modelo;
Crie uma nova coluna chamada grupo contendo o cluster atribuído a cada usuário;
Exiba as primeiras linhas do DataFrame atualizado.
"""
modelo = KMeans(n_clusters=4, random_state=42)
matriz_kmeans = dataframe[["horas_semana", "dias_acesso_mes"]] # precisa do [[]] para não virar tupla
dataframe["grupo"] = modelo.fit_predict(matriz_kmeans)
print(dataframe.head(10))

"""
Parte 4 – Avaliação da Clusterização:
Calcule o Silhouette Score da clusterização obtida;
Apresente o valor encontrado.
"""
score = silhouette_score(matriz_kmeans, dataframe["grupo"])
print("O score silhouette é:", score)


"""                               
Parte 5 – Visualização dos Clusters:
Crie um gráfico de dispersão contendo:
os usuários coloridos conforme o grupo encontrado;
os centróides identificados pelo algoritmo.
Observe o resultado gerado.
"""
plot.scatter(dataframe["horas_semana"], dataframe["dias_acesso_mes"], dataframe["grupo"])
plot.xlabel("horas_semana")
plot.ylabel("dias_acesso_mes")
centroides = modelo.cluster_centers_
plot.scatter(centroides[:,0], centroides[:,1], c="red")

plot.show()





"""

Questões de Interpretação analítica.
O valor do Silhouette Score indica uma clusterização ruim, razoável ou boa? Justifique sua resposta.
Descreva os perfis de usuários encontrados nos grupos. Exemplo: "Grupo X: usuários com poucos acessos e poucas horas de utilização."
De que forma a empresa poderia utilizar os grupos encontrados para melhorar seus serviços ou campanhas de marketing?

Desafio adicional: 
Repita a clusterização utilizando K = 3, K = 5;
Calcule o Silhouette Score para cada caso e preencha a tabela.

Silhouette Score:
3 -
4 - 0.6947582909201341
5 -



Qual valor de K parece representar melhor os dados? Justifique sua resposta.

Exercício 2: Aprendizado Supervisionado com Árvores de Decisão.
Objetivo: Neste exercício, você utilizará um algoritmo de Aprendizado Supervisionado para construir um modelo capaz de prever se um usuário realizará ou não uma compra em uma loja virtual.
Contextualização: Uma empresa de comércio eletrônico deseja compreender melhor o comportamento dos visitantes de seu site. Para isso, foi disponibilizado um conjunto de dados contendo informações sobre usuários que acessaram a plataforma. Cada registro possui os seguintes atributos: idade, paginas_visitadas, tempo_site, produtos_visualizados, carrinho (0 = vazio, 1 = com itens), compra (0 = não concluiu, 1 = concluiu). Este último será usado como classe. Seu objetivo é criar um modelo capaz de prever essa variável com base nos demais atributos.
Utilize o arquivo fornecido pelo professor: Exercicio-DT-clientes-ecommerce.csv
Parte 1 – Exploração dos Dados:
Carregue o arquivo CSV utilizando a biblioteca Pandas.
Exiba as cinco primeiras linhas do conjunto de dados.
Informe a quantidade de registros e quantidade de atributos.
Parte 2 – Preparação dos Dados:
Defina as variáveis de entrada (X) utilizando os atributos: idade, paginas_visitadas, tempo_site, produtos_visualizados, carrinho.
Defina a variável alvo (y): compra
Divida os dados em conjuntos de treinamento e teste utilizando: 70% para treinamento; 30% para teste.
Parte 3 – Treinamento do Modelo:
Importe o algoritmo de Árvore de Decisão.
Crie o modelo.
Treine o modelo utilizando os dados de treinamento.
Parte 4 – Realizando Previsões:
Utilize o modelo treinado para prever os dados do conjunto de teste.
Exiba as previsões obtidas.
Parte 5 – Avaliação do Modelo:
Calcule a acurácia do modelo.
Apresente o valor obtido.
Qual o valor da acurácia encontrada?
Parte 6 – Interpretação dos Resultados:
A acurácia obtida foi satisfatória? Justifique sua resposta.
Qual é a função da divisão entre conjunto de treinamento e conjunto de teste?
Explique, com suas palavras, como uma árvore de decisão realiza classificações.
Observando os atributos disponíveis, qual deles você acredita que possui maior influência na decisão de compra? Justifique sua resposta.
Parte 7: Implantação: Utilize o modelo treinado para prever o comportamento de novos usuários.


idade
paginas visitadas
tempo no site
produtos visualizados
carrinho
Previsão de compra
usuário A
31
12
10
8
1


usuário B
24
5
4
3
0



Quais os resultados das previsões de comportamento dos usuários A e B?
Desafio adicional: Visualize a árvore de decisão utilizando a função plot_tree() e responda:
Qual atributo aparece na raiz da árvore?
Esse atributo faz sentido para o problema estudado?
O resultado está de acordo com a hipótese levantada na Questão 4?


"""