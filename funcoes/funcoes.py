from pandas import read_csv

#Obtem os pontos (as cidades) que fazem parte da rota
def CidadesRota(dados):
    cidades = []
    cid = dados.columns
    for i in cid:
        cidades.append(str(i))
    return cidades

#Fazer a distribuicao de Frequencia
def CriarMatriz(valor):
    matriz = []
    dados = read_csv(valor)
    #obtem as cidades da rota
    cidades = CidadesRota(dados)
    dados = dados.values
    for i in range(len(dados)):
        x = []
        for g in dados[i]:
            x.append(float(g))
        matriz.append(x)
    #retorna a matriz e a rota inicial
    return matriz, cidades

#Cria vetor de inteiros que representa a rota inicial
def EnumerarCidades(cidades):
    x = []
    for i in range(len(cidades)):
        x.append(i)
    return x

#Avalia o custo da rota
def Avalia(rota, matriz):
    custo = 0
    for i in range(len(rota)-1):
        custo = custo + matriz[rota[i]][rota[i+1]]
    #soma o custo para retornar ao ponto inicial
    custo = custo + matriz[rota[len(rota)-1]][rota[0]]
    return custo

# ORDENAR EM DECRESCENTE AS APTIDOES
def OrdenarAptidoes(apt, apt_desc, popu, cruza):
    pop_ini = []
    desc = []
    apt_p_ini = apt
    apt_p_des = apt_desc
    apt_p_ini.sort(reverse=True)
    apt_p_des.sort(reverse=True)
    for i in apt_p_ini:
        x = apt.index(i)
        pop_ini.append(popu[x])
    for i in apt_p_des:
        x = apt_desc.index(i)
        desc.append(cruza[x])
    return apt_p_ini, apt_p_des, pop_ini, desc

#ORDENAR EM DECRESCENTE A POPULACAO DE ACORDO COM A APTIDAO
def Ordenar(apt_atual, popu):
    populacao = []
    apt = apt_atual
    apt.sort(reverse=True)
    for i in apt:
        x = apt_atual.index(i)
        populacao.append(popu[x])
    return apt, populacao