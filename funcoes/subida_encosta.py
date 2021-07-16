from funcoes.funcoes import Avalia
from random import randint
from copy import deepcopy

#metodo que calcula a subida de encosta ALTERADA
#recebe: rota inicial, matriz de valores, custo inicial
def Subida_Enc_Alt(inicial, matriz, dist):
    atual = deepcopy(inicial) #copia a sequencia inicial de pontos
    val_at = dist #custo da sequencia atual
    cont = 0 #contador tentativas
    tent = len(inicial)

    ordem = 1
    while True:
        prox = Sucessores(atual, matriz, dist)
        vp = Avalia(prox, matriz)
        ordem = ordem + 1
        if vp>=val_at:
            if cont<tent:
                cont += 1
            else:
                break
        else:
            atual = prox
            val_at = vp
    
    return atual, val_at

#Cria novas combinacoes
def Sucessores(atual, matriz, dist):
    melhor = deepcopy(atual)
    val_me = dist
    ponto_ale = randint(0, len(atual)-1)

    for i in range(len(atual)):
        novo_atual = deepcopy(atual)
        x = novo_atual[i]
        novo_atual[i] = novo_atual[ponto_ale]
        novo_atual[ponto_ale] = x
        val_novo = Avalia(novo_atual, matriz)
        if val_novo<val_me:
            val_me = val_novo
            melhor = novo_atual
    
    return melhor