import funcoes.funcoes as fc #metodos internos
from sklearn.utils import shuffle

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