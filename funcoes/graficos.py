from streamlit import bar_chart, plotly_chart
from pandas import DataFrame
import plotly.express as px

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
    #bar_chart(df["Custo"])
    graf = px.pie(
        df,
        values="Custo",
        names=["Custo Inicial","Custo Final"],
        title="Comparação:"
    )
    plotly_chart(graf)