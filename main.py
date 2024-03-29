#Import principal
import streamlit as st
#Import relacionado
from pandas import read_csv, DataFrame
import webbrowser
#Import metodos internos
import funcoes.funcoes as fc
import funcoes.genetico as gn
import funcoes.subida_encosta as sb
import funcoes.documentar as dc
import funcoes.graficos as gf


class ProLinear:

    def __init__(self):
        self.n_rota = [] #Recebe a nova rota
        self.popu = [] #Matriz para populacao inicial
        self.n_popu = [] #recebe a nova popu. depois da mutacao
        self.desc = [] #matriz com os descendentes (resultado do Cruzamento)
        self.apt = [] #aptidao  dos individuos
        self.apt_desc = [] #aptidao dos ind. retornados da mutacao
        self.Matriz = [] #Matriz com as distan. entre as cidades
        self.RotaIni = [] #Vetor com as cidades que fazem parte da rota
        self.resul = 0 #valor do custo da rota inicial
        self.n_custo = 0 #valor do custo final
        self.ID_cidades = [] #Vetor com inteiro para ID cada cidade da rota inicial
        self.TP = [20, 50] #tam da populacao
        self.NG = [20, 100] #numero de geracoes
        self.IG = [0.1, 0.2] #intervalo de geracao
        self.TM = [0, 0.1] #taxa de mutacao
        self.TC = [0.5, 0.7, 0.8] #taxa de cruzamento

        st.set_page_config(page_title='ProLinear', page_icon="imagens/ProLinear.png")
        self.opcoes = ["Selecione","Otimizar rota"]

    def Inicial(self):
        st.title("ProLinear")
        acao = st.sidebar.selectbox("Opções", self.opcoes)
        if acao==self.opcoes[1]:
            self.EntradaDados()
    
    #Faz a entrada de dados para o programa
    def EntradaDados(self):
        st.write("Otimizar rota.")
        dados = st.file_uploader("Selecione um arquivo .CSV (separado por vírgula) com os dados de distância:", accept_multiple_files=True, type=["csv"])
        if dados:
            self.Matriz, self.RotaIni = fc.CriarMatriz(dados[0])
            self.ID_cidades = fc.EnumerarCidades(self.RotaIni)
            self.resul = fc.Avalia(self.ID_cidades, self.Matriz)

    #Responsavel pelas funcoes de otimizacao da rota
    def OtimizarRota(self, tp, ng, tc, tm, ig):
        self.tp = tp #tam da populacao
        self.ng = ng #numero de geracoes
        self.ig = ig #intervalo de geracao
        self.tm = tm #taxa de mutacao
        self.tc = tc #taxa de cruzamento
        
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
        self.NovaRota() #retornar a nova rota, melhor que a inicial

        return self.n_rota, self.n_custo
    
    #Gerar populacao inicial
    def PopuInicial(self):
        self.popu = gn.Populacao_Inicial(self.ID_cidades, self.tp)
    
    #Calcular aptidao de cada individuo
    def AptidaoIndividuos(self, individuos):
        soma_apt = 0
        self.apt = gn.Aptidao(individuos, self.tp, self.Matriz)
    
    #Gerar os descendentes da populacao
    def GerarDescendentes(self):
        self.desc = gn.Cruzamento(self.popu, self.apt, self.tc)
    
    #Faz mutacao entre os descendentes mais aptos
    def Mutacao(self):
        self.desc = gn.MutacaoGene(self.popu, self.desc, self.tm)
    
    #Aptidao dos individuos retornados da Mutacao
    def AptidaoDescendentes(self):
        soma = 0
        self.apt_desc = gn.Aptidao(self.desc, len(self.desc), self.Matriz)
    
    #Coloca em ordem decrescente a apt. da popu inicial e dos desc.
    def Ordenar(self):
        self.apt, self.apt_desc, self.popu, self.desc = fc.OrdenarAptidoes(self.apt, self.apt_desc, self.popu, self.desc)
    
    #Gera os novos individuos da populacao apos a mutacao
    def NovaPopu(self):
        self.n_popu = gn.Nova_popu(self.popu, self.desc, self.ig)
    
    #ordena em decrescente: apt_desc e nova popu.
    def OrdenarAtual(self):
        self.apt_desc, self.n_popu = fc.Ordenar(self.apt, self.n_popu)
    
    #retornar nova rota, melhor que a atual
    def NovaRota(self):
        cid_rota = []
        self.n_rota = self.n_popu[len(self.popu)-1]
        self.n_custo = fc.Avalia(self.n_rota, self.Matriz)
    
    def Persistencia(self):
        cid_rota = [] #vetor das rotas
        rota = [] #vetor para receber a rotafinal
        custo = [] #vetor de custos das rotas
        #testa diferentes parametros geneticos
        for i1 in range(len(self.TP)):
            for i2 in range (len(self.NG)):
                for i3 in range(len(self.TC)):
                    for i4 in range(len(self.TM)):
                        for i5 in range(len(self.IG)):
                            r, c = self.OtimizarRota(self.TP[i1],self.NG[i2],self.TC[i3],self.TM[i4],self.IG[i5])
                            rota.append(r)
                            custo.append(c)
        rota, custo = fc.OrdenarResultado(rota, custo) #reordenado a rota com base no custo
        dist = custo #recebe os custos
        
        try:
            #realiza a Subida de Encosta Alterada
            rota_sub_enc, custo_sub_enc = sb.Subida_Enc_Alt(self.ID_cidades, self.Matriz, self.resul)
            #se os algoritmos forem melhores ou iguais...
            if custo[0]<=custo_sub_enc:
                for i in rota[0]:
                    cid_rota.append(self.RotaIni[i])
                custo = custo[0]
            #se a subida de encosta encontrar resultado melhor...
            else:
                for i in rota_sub_enc:
                    cid_rota.append(self.RotaIni[i])
                custo = custo_sub_enc
            fc.MostraResultado(cid_rota, custo)
            gf.Custos(dist)
            gf.CompararCustos(custo, self.resul)
            dc.GerarPDF(cid_rota)
            webbrowser.open("ProLinear.pdf")
        
        except:
            st.error("Não fez subida de Encosta nem gerou gráficos.")

pro = ProLinear()
pro.Inicial()
try:
    pro.Persistencia()
except:
    pass