from streamlit import bar_chart, plotly_chart, line_chart, pyplot
from pandas import DataFrame
from random import randint
import matplotlib.pyplot as plt
import plotly.express as px

#Exibe a variacao dos custos das rotas
def Custos(custos):
    y = []
    c = []
    cont = 0
    for i in reversed(custos):
        cont+=1
        y.append(cont)
        c.append(i)
    plt.xlabel("Tentativa (º)")
    plt.ylabel("Custo da rota")
    plt.title("Custos calculados")
    plt.scatter(y, c)
    plt.plot(y, c)
    plt.axis([1, len(c), min(c)-100, max(c)+100])
    pyplot(plt)

#Recebe ocusto final e o iniciale faz a comparacao
def CompararCustos(custo_f, custo_i):
    dados = [custo_i, custo_f]
    df = DataFrame(dados, columns=["Custo"])
    graf1 = px.bar(
        df,
        x="Custo",
        y=["Custo Inicial","Custo Final"],
        title="Comparação do custo das rotas:",
        color_continuous_scale=True
    )
    plotly_chart(graf1)