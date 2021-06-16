from sklearn.utils import shuffle

#Metodo parar gerar a populacao inicial
def Populacao_Inicial(lista_pontos, tam_pop):
	popu = []
	for i in range(tam_pop):
		n_lista = lista_pontos
		popu.append(shuffle(n_lista))
	return popu