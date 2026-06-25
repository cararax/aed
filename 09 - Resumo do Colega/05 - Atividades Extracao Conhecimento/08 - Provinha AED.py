import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns # trabalha em cima do matplotlib, então usar matplotlib é interchangeable com seaborn

# Primeiro carregamos o csv (atividades 1):

df = pd.read_csv("11 - Dados - Tips.csv")

def parte_1(df):
    print(df.head(n=10),"\n")
    print(df.isna().any().any(), "\n")
    print(df.info(),"\n")
    print(df.describe(),"\n")
    '''
    Os dados parecem adequados vendo no .info, não temos valores nulos então não precisamos de tratamento em relação a isso
    Além disso, os dados parecem adequados. Não vejo como fumar ajuda ou não em gorjetas, mas nunca se sabe, talvez faça diferença.
    mesmo que de maneira superficial, podem nos mostrar um padrão antes escondido, por exemplo a saúde do indivíduo e daí, sua "generosidade"

    A média e mediana parecem ser bem parecidas inicialmente, mas um ponto a considerar é o size que está na média e na mediana. Mesmo que
    a média diga que o size tende mais a ser um 3, a mediana volta com um size 2. Parece indicar então que o size como média está considerando
    valores grandes em comparação com valores pequenos e mais comuns e assim, inflando seu valor de size médio "real", mesmo tendo o size 2
    como um size mais comum que 3.
    '''


parte_1(df)


def parte_2(df): 
    tip_pct = df.tip.div(df.total_bill)
    print(tip_pct.head())

    print(df.smoker.value_counts())

    sns.countplot(
            x='day',
            data=df
        )

    plt.title('count plot por dia')
    plt.xlabel('dia')
    plt.show() 
    # por questões de tempo, vou parar de fazer ficar bonitinho com titulo e tudo mais

    sns.histplot(data=df, x="total_bill", kde=True)
    plt.show()

    top_10 = (df.total_bill.sort_values(ascending=False)).head(n=10)
    print(top_10)


    mesas_estranhas = (tip_pct > 0.30)
    print(mesas_estranhas[mesas_estranhas])
    '''
    Podemos ver que as 10 maiores contas não foram as contas com a maior gorjeta, então o nível de gasto maior não equivale a gorjetas maiores.
    Agora, a mesa 154 e 344 são atípicas, um padrão nelas é que ambos são homens não fumantes com gastos muito similares e mesmo size no mesmo dia.
    É muito provável que seja a mesma pessoa. Além disso, o que ele comeu não é muito caro nem grande, sua gorjeta também não é "grande", mas
    em proporção ao custo de sua comida, acaba se tornando. E claro, a gorjeta é igual, talvez seja o jeito dessa pessoa especifica em fornecer
    gorjeta, caso seja uma pessoa só, considerando uma rotina.
    '''




parte_2(df)

def parte_3(df):
    tip_pct = df.tip.div(df.total_bill)
    #print(tip_pct.axes)
    sns.scatterplot(x="total_bill", y="tip", data=df)
    plt.show()

    merge_data_frames = pd.concat([tip_pct, df], axis=1)
    #print(merge_data_frames.head())
    nomes = ['media', 'total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']
    merge_data_frames.columns = nomes

    sns.barplot(data=merge_data_frames, x="sex", y="media")
    plt.show()

    media_por_dia = merge_data_frames.sort_values(["media"]).groupby("day")
    print(media_por_dia.head(n=5))
    '''
    Ao que tudo indica, acredito ser uma relação fraca, vemos uma leve rampa subindo nos valores da gorjeta, considerando 
    o valor da comida e a gorjeta dada por ela, a relação entre as pessoas que pagaram 50 na bill e outras que pagaram 10, podem ter
    gorjetas iguais (por mais que algumas que pagaram 50 tenham bastante gorjeta comparativamente).

    Não parece ter uma diferença extremamente significativa, apenas de uns 2,5% aproximadamente entre relação homem x mulher. Em
    questão de precisão, faz diferença, mas no geral, acredito ser negligível, não é confirmado a relação, o dataset é pequeno.
    
    '''

parte_3(df)


# Parte 4, fora da função mesmo, direto aqui ################################
sns.scatterplot(x="total_bill", y="tip", data=df, hue = "smoker")
plt.show()

media_absoluta = df.groupby(["day", "time"])[["tip"]].mean()
print(media_absoluta.head())
plt.clf()
sns.barplot(data=media_absoluta, x="day", y="tip", hue="time")
plt.show()

'''
Sunday e Saturday são os melhores dias para esses garçons, além disso, os dinners são de maior gorjeta que os lunch, logo em
dinners e sunday e saturday são os melhores dias e horários para esses garçons.

Fumantes parecem gastar mais que os demais, mas também não costumam por gastar mais, oferecer necessariamente mais gorjeta. Tirando
o top 1 gorjeta que venho de um fumante. Parece então, que em questão de lucros, eles são gastadores mais veementes, que nem sempre
oferecem uma gorjeta em porcentagem similar ao que gastam. Fumantes são bons pro negócio, nem tão bons pros garçons (levemente)

'''

