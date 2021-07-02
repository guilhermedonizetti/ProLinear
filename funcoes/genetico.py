import funcoes.funcoes as fc #metodos internos
from sklearn.utils import shuffle
from math import ceil
from random import randrange, uniform

#Metodo parar gerar a populacao inicial
def Populacao_Inicial(lista_pontos, tam_pop):
	popu = []
	for i in range(tam_pop):
		n_lista = lista_pontos
		popu.append(shuffle(n_lista))
	return popu

#Calcular a aptidao de cada individuo
def Aptidao(populacao, tam_pop, matriz):
	freq = []
	soma = 0
	for i in range(tam_pop):
		custo = fc.Avalia(populacao[i], matriz)
		freq.append(1/custo)
		soma = soma + (1/custo)
	for i in range(tam_pop):
		freq[i] = freq[i]/soma
	return freq

#Metodo para cruzar os pais (individuos) selecionados
def Cruzamento(populacao,aptid,tc):
    desc = []
    tam1 = len(populacao)
    qc = ceil(tc*tam1)

    tam2 = len(populacao[0])
    corte = randrange(1,tam2)

    for i in range(qc):
        # escolhe pai 1
        p1 = Roleta(aptid)

        # escolhe pai2
        p2 = Roleta(aptid)

        #descendente 1
        linha = []
        for g in range(corte):
            linha.append(populacao[p1][g])
        for g in range(corte,tam2):
            linha.append(populacao[p2][g])
        desc.append(linha)

        #descendente 2
        linha = []
        for g in range(corte):
            linha.append(populacao[p2][g])
        for g in range(corte,tam2):
            linha.append(populacao[p1][g])
        desc.append(linha)

    # ajusta descendentes para atender a restrição do problema
    for i in range(2*qc):
        aux = list(range(0,tam2))
        for j in range(0,corte):
            aux.remove(desc[i][j])
        j = corte
        while(len(aux)>0):
            if(desc[i].count(aux[0])==0):
                if(desc[i].count(desc[i][j])>1):
                    desc[i][j] = aux[0]
                    del aux[0]
                    j += 1
                else:
                    j += 1
            else:
                del aux[0]

    return desc

#Metodo para selecionar dois individuos (pais) para cruzamento
def Roleta(aptidao):
    soma = 0
    p = 0
    aleat = uniform(0,1)
    while soma<aleat:
        soma = soma + aptidao[p]
        p = p+1
    p = p - 1
    return p

# METODO DE MUTACAO ENTRE OS MAIS APTOS
def MutacaoGene(pop,desc,tm):
    tam1 = len(pop)
    qm = ceil(tm*tam1)

    tam2 = len(desc)

    for i in range(qm):
        # escolhe descendente
        ind = randrange(tam2)
        aux = []
        aux = desc[ind]
        # inverte o primeiro e o ultimo elemento
        aux_p = aux[0]
        aux_u = aux[len(aux)-1]
        aux[0] = aux_u
        aux[len(aux)-1] = aux_p
        desc.append(aux)
    return desc

# Funcao para gerar a nova populacao
def Nova_popu(pop,desc,ig):
    tam = len(pop)
    elite = ceil(ig*tam)
    for i in range(elite,tam):
        pop[i] = desc[i-elite]
    return pop