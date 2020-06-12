from statistics import mean, stdev
from estatistica_descritiva import distribuicao, moda, separa_up_down

# funcao fitness para
def fitness(vetor, vetor_ref, vetor_peso):
    Fitness = 0.0
    for i in vetor_ref:
        Fitness=Fitness+vetor_peso[i]*((vetor[i]-vetor_ref[i])**2)
    #Fitness_medio = Fitness/len(vetor_ref)
    return Fitness


def fitness_populacao(Populacao_ga):
    fitness_lista =[]
    for i in Populacao_ga:
        fitness_lista.append(Populacao_ga[i]['fitness'])

    fitness_media = mean(fitness_lista)
    fitness_desvio = stdev(fitness_lista)

    lista_up_down = separa_up_down(fitness_lista, fitness_media)

    contador_up = len(lista_up_down['up'])
    if contador_up==1:
        desvio_up = 1
    else:
        desvio_up = stdev(lista_up_down['up'])

    contador_down = len(lista_up_down['down'])
    if contador_down==1:
        desvio_down = 0
    else:
        desvio_down = stdev(lista_up_down['down'])

    distribuicao_fitness = distribuicao(fitness_lista, 100)
    moda_vetor = moda(distribuicao_fitness)
    moda_valor = moda_vetor['moda']

    # print(distribuicao_fitness)

    return {'media': fitness_media,
            'moda':moda_valor,
            'desvio':fitness_desvio,
            'contador_up': contador_up,
            'contador_down': contador_down,
            'desvio_up': desvio_up,
            'desvio_down': desvio_down,
            'distribuicao':distribuicao_fitness
            }



#r= fitness({'q':1,'w':2,'e':3}, {'q':11,'w':33,'e':22},  {'q':10,'w':1,'e':1})
#print(r)