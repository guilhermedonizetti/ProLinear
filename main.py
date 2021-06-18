import streamlit as st
#metodos internos
import funcoes.funcoes as fc
import funcoes.genetico as gn
from pandas import read_csv

class ProLinear:

    def __init__(self):
        self.popu = [] #Matriz para populacao inicial
        self.apt = [] #aptidao  dos individuos
        self.Matriz = [] #Matriz com as distan. entre as cidades
        self.RotaIni = [] #Vetor com as cidades que fazem parte da rota
        self.ID_cidades = [] #Vetor com inteiro para ID cada cidade da rota inicial
        self.TP = 20 #tam da populacao
        self.NG = 50 #numero de geracoes
        self.IG = 0.1 #intervalo de geracao
        self.TM = 0.4 #taxa de mutacao
        self.TC = 0.5 #taxa de cruzamento

        st.set_page_config(page_title='ProLinear', page_icon="imagens/ProLinear.png")
        self.opcoes = ["Selecione","Otimizar rota"]

    def Inicial(self):
        st.title("ProLinear")
        acao = st.sidebar.selectbox("Opções", self.opcoes)
        if acao==self.opcoes[1]:
            self.OtimizarRota()
    
    #Responsavel pelas funcoes de otimizacao da rota
    def OtimizarRota(self):
        st.write("Otimizar rota.")
        dados = st.file_uploader("Selecione um arquivo .CSV (separado por vírgula) com os dados de distância:", accept_multiple_files=True, type=["csv"])
        if dados:
            self.Matriz, self.RotaIni = fc.CriarMatriz(dados[0])
            self.ID_cidades = fc.EnumerarCidades(self.RotaIni)
            resul = fc.Avalia(self.ID_cidades, self.Matriz)
            st.write("Rota inicial passa pelas cidades {} e retorna à {}".format(self.RotaIni, self.RotaIni[0]))
            st.info("Custo da rota inicial: {}".format(resul))
            #Chama os metodos do algoritmo genetico
            self.PopuInicial() #gerar a populacao inicial
            self.AptidaoIndividuos() #calcular a aptidao de cada individuo
    
    #Gerar populacao inicial
    def PopuInicial(self):
        self.popu = gn.Populacao_Inicial(self.ID_cidades, self.TP)
        st.write("População inicial: ")
        st.dataframe(self.popu)
    
    #Calcular aptidao de cada individuo
    def AptidaoIndividuos(self):
        soma_apt = 0
        self.apt = gn.Aptidao(self.popu, self.TP, self.Matriz)
        for i in self.apt:
            soma_apt+=i
        st.json(self.apt)
        st.write("A soma das aptidões é: {}".format(soma_apt))

pro = ProLinear()
pro.Inicial()