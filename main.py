import streamlit as st
#metodos internos
import funcoes.funcoes as fc
import funcoes.genetico as gn
from pandas import read_csv

class ProLinear:

    def __init__(self):
        self.popu = [] #Matriz para populacao inicial
        self.n_popu = [] #recebe a nova popu. depois da mutacao
        self.desc = [] #matriz com os descendentes (resultado do Cruzamento)
        self.apt = [] #aptidao  dos individuos
        self.apt_desc = [] #aptidao dos ind. retornados da mutacao
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
            self.AptidaoIndividuos(self.popu) #calcular a aptidao de cada individuo
            self.GerarDescendentes() #gera os descendentes dos individuos: Cruzamento
            self.Mutacao() #faz mutacao entre os descendentes mais aptos
            self.AptidaoDescendentes() #Aptidao dos individuos retornados da Mutacao
            self.Ordenar() #coloca em ordem decrescente: apt. popu. inicial dos descendentes
            self.NovaPopu() #gera os novos individuos da populacao apos a mutacao
            self.AptidaoIndividuos(self.n_popu) #calcula a aptidao dos indiv. da nova popu.
            self.OrdenarAtual() #ordena em decrescente: apt_desc e nova popu.
    
    #Gerar populacao inicial
    def PopuInicial(self):
        self.popu = gn.Populacao_Inicial(self.ID_cidades, self.TP)
        st.write("População inicial: ")
        st.dataframe(self.popu)
    
    #Calcular aptidao de cada individuo
    def AptidaoIndividuos(self, individuos):
        soma_apt = 0
        self.apt = gn.Aptidao(individuos, self.TP, self.Matriz)
        for i in self.apt:
            soma_apt+=i
        st.json(self.apt)
        st.write("A soma das aptidões é: {}".format(soma_apt))
    
    #Gerar os descendentes da populacao
    def GerarDescendentes(self):
        self.desc = gn.Cruzamento(self.popu, self.apt, self.TC)
        st.write("Descendentes: ")
        st.dataframe(self.desc)
    
    #Faz mutacao entre os descendentes mais aptos
    def Mutacao(self):
        self.desc = gn.MutacaoGene(self.popu, self.desc, self.TM)
        st.write("Resultado da Mutação:")
        st.dataframe(self.desc)
    
    #Aptidao dos individuos retornados da Mutacao
    def AptidaoDescendentes(self):
        soma = 0
        self.apt_desc = gn.Aptidao(self.desc, len(self.desc), self.Matriz)
        for i in self.apt_desc:
            soma+=i
        st.json(self.apt_desc)
        st.write("A soma das aptidões é: {}".format(soma))
    
    #Coloca em ordem decrescente a apt. da popu inicial e dos desc.
    def Ordenar(self):
        self.apt, self.apt_desc, self.popu, self.desc = fc.OrdenarAptidoes(self.apt, self.apt_desc, self.popu, self.desc)
    
    #Gera os novos individuos da populacao apos a mutacao
    def NovaPopu(self):
        self.n_popu = gn.Nova_popu(self.popu, self.desc, self.IG)
        st.write("Resultado da nova população: ")
        st.dataframe(self.n_popu)
    
    #ordena em decrescente: apt_desc e nova popu.
    def OrdenarAtual(self):
        st.write("Estrutura de dados antes da ordenação: ")
        st.json(self.apt)
        st.json(self.n_popu)
        self.apt_desc, self.n_popu = fc.Ordenar(self.apt, self.n_popu)
        st.write("Aptidão e N. População ordenados em decrescentes:")
        st.json(self.apt)
        st.dataframe(self.n_popu)

pro = ProLinear()
pro.Inicial()