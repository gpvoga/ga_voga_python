
import random
import modelo_teste
import fitness
import csv
import keyboard
from statistics import mean, stdev
from estatistica_descritiva import distribuicao, moda

class GA_VOGA(object):

    def __init__(self):
        # definicao de parametros do modelo que sera otimizado
        self.parametro_modelo = ['a', 'b', 'c', 'd']

        self.vetor_parametro={'a':[-10.0, 10.0, 0.0001],
                              'b':[-10.0, 10.0, 0.0001],
                              'c':[-10.0, 10.0, 0.0001],
                              'd':[-10.0, 10.0, 0.0001]}
        self.vetor_ref={'a':4, 'b':-2,'c':-7,'d':10}
        self.vetor_peso={'y_media':1, 'y_desvio':1, 'dy_media':1, 'dy_desvio':1, 'd2y_media':1,'d2y_desvio':1}
        self.espaco_simulacao = {'xi':-10, 'xf':10, 'passo':0.01}

        # definicao de parametros do algoritmo genetico
        self.n_pop = 500
        self.otimizador='minimo'                # meta do GA minimiza ou maximizar o problema
        self.predador_tipo='distribuicao'       # tipo de predados utilizado no GA {ftness_media, fitness_distribuicao}
        self.predador_desvio_tipo='desvio_down'
        self.fitness_ref ='moda'                # parametros de acompanhamento da populacao (mostra na tela)
        self.predador_n_desvio=1                # fitness_media --> quantidade de desvio que serão usados no corte de individuos = media + n_desvio*desvio
        self.predador_frequencia_corte= 0.6     # percentiual limite para o corte de individuos
        self.max_prob=1000                      # faixa total para selecao aleatoria do operador genetico
        self.prob_imigrante=100                  # taxa limite de individuos criados elatoriamente 10/1000
        self.prob_mutante=200                  # taxa de individuos criados por mutacao 60/1000
        self.tick_mutante=20                    # faixa maxima de alteração do opetrador mutante
        self.prob_downhill= 500                 # Taxa de individuso otimizado por down-hill
        self.prob_crossover=1000                # taxa de cross over
        self.file = open('ga_evolucao.csv', 'w',  newline='')
        self.file_ga_evolucao = csv.writer(self.file,  delimiter=';')


    ############################################################################
    #
    # inicio do processo de otimização do ga
    #
    #############################################################################
    def ga_voga(self):

        modelo_referencia = modelo_teste.modelo(self.espaco_simulacao, self.vetor_ref)

        # cria a populacao inicial
        Populacao_inicial = self.cria_populacao_inicial(self.n_pop)

        # calcula o fitness de cada individuo sem o fitness presente
        Populacao_ga = self.calcula_fitness(Populacao_inicial, modelo_referencia)

        #print(Populacao_inicial)
        #print(Populacao_ga)

        self.ga_loop(Populacao_ga, modelo_referencia)

        return 1

    ##########################################################################
    #
    # Loop de interração do ga
    # o sistema manipula a populacao
    def ga_loop(self, Populacao_ga, modelo_referencia):
        # loops do ga
        for geracao in range(0,1000,1):
            Fitness_populacao = fitness.fitness_populacao(Populacao_ga)

            # operadores geneticos
            predador_lista=self.predador(Populacao_ga, Fitness_populacao)

            solucao_aquiles = self.solucao_aquiles(Populacao_ga)
            fitness_aquiles = solucao_aquiles['fitness']
            Aquiles =  solucao_aquiles['aquiles']
            config_aquiles = solucao_aquiles['config']

            print('geracao:', geracao, '| predador:', len(predador_lista), '| fitness:', Fitness_populacao[self.fitness_ref], ' | desvio:', Fitness_populacao[self.predador_desvio_tipo],' | Aquiles ', Aquiles, fitness_aquiles, config_aquiles)

            self.file_ga_evolucao.writerow([geracao,len(predador_lista),Fitness_populacao[self.fitness_ref],Fitness_populacao[self.predador_desvio_tipo], Aquiles, fitness_aquiles, config_aquiles])
            Populacao_ga= self.operador_genetico(Populacao_ga,predador_lista, modelo_referencia)
            Populacao_ga = self.calcula_fitness(Populacao_ga, modelo_referencia)

    ###########################################################################################
    #
    # lista de operadores geneticos para corte de individuos oou criacao de novos individuos
    #
    ###########################################################################################

    def predador(self, Populacao_ga, Fitness_populacao):
        predador_lista = []
        # predador baseado no desvio da media
        if self.predador_tipo=='fitness_media':
            media = Fitness_populacao['media']
            desvio_tipo = self.predador_desvio_tipo
            desvio = Fitness_populacao[desvio_tipo]

            limite_predador = media+desvio*self.predador_n_desvio

            for i in Populacao_ga:
                if self.otimizador =='minimo' and Populacao_ga[i]['fitness'] > limite_predador:
                    predador_lista.append(i)
                elif  self.otimizador =='maximo' and Populacao_ga[i]['fitness'] < limite_predador:
                    predador_lista.append(i)

            if predador_lista ==[]:
                print('ativar: genocidio')
                for i in Populacao_ga:
                    limite_predador = media
                    if self.otimizador == 'minimo' and Populacao_ga[i]['fitness'] > limite_predador:
                        predador_lista.append(i)
                    elif self.otimizador == 'maximo' and Populacao_ga[i]['fitness'] < limite_predador:
                        predador_lista.append(i)
            #print('media', predador_lista, len(predador_lista))

        elif self.predador_tipo == 'distribuicao':
            predador_lista = []
            distribuicao_fitness = Fitness_populacao['distribuicao']

            # define o limite do fitness de corte
            for k_distribuicao in distribuicao_fitness:
                frequencia_acu = distribuicao_fitness[k_distribuicao]['frequencia_acu']
                if frequencia_acu > self.predador_frequencia_corte:
                    limite_predador = distribuicao_fitness[k_distribuicao]['media']
                    break

            for i in Populacao_ga:
                if self.otimizador == 'minimo' and Populacao_ga[i]['fitness'] > limite_predador:
                    predador_lista.append(i)
                elif self.otimizador == 'maximo' and Populacao_ga[i]['fitness'] < limite_predador:
                    predador_lista.append(i)
            #print('media', predador_lista, len(predador_lista))

        return predador_lista

    ##########################################################################
    # gerencia a execução dos operadores geneticos

    def operador_genetico(self, Populacao_ga, Predador_lista, modelo_referencia):
        Populacao_ga = self.op_morte(Predador_lista, Populacao_ga)

        for Individuo_morte in Predador_lista:
            prob_random = random.uniform(0, 1000)
            if prob_random < self.prob_imigrante:
                Populacao_ga = self.op_imigrante(Individuo_morte, Populacao_ga)
            elif prob_random < self.prob_mutante:
                Populacao_ga = self.op_mutante(Individuo_morte, Populacao_ga)
            elif prob_random < self.prob_downhill:
                Populacao_ga = self.op_downhill(Individuo_morte, Populacao_ga, modelo_referencia)
            elif prob_random < self.prob_crossover:
                Populacao_ga = self.op_crossover(Individuo_morte, Populacao_ga)
        return Populacao_ga


    #############################################################################
    # elimina todos os individuos selecionados pelo op morte
    def op_morte(self, Individuo_lista, Populacao_ga):
        for Individuo in Individuo_lista:
            del Populacao_ga[Individuo]
        return Populacao_ga


    #############################################################################
    # cria um novo individuo aletaorioamente e coloca- na ppopulacao
    def op_imigrante(self, Individuo, Populacao_ga):
        Populacao_ga[Individuo]=self.cria_individuo()
        return Populacao_ga

    # realiza uma mutacao pontual em um individuo
    def op_mutante(self, Individuo, Populacao_ga):
        Individuo_mutante = random.choice(list(Populacao_ga.keys()))
        posicao_mutante = random.choice(list(self.parametro_modelo))
        #print(Individuo_mutante, Populacao_ga[Individuo_mutante])
        Populacao_ga[Individuo]={}
        for p in self.parametro_modelo:
            if p==posicao_mutante:
                valor = Populacao_ga[Individuo_mutante][p]
                delta_mutacao= self.vetor_parametro[p][2]
                mutacao = delta_mutacao*random.uniform(-self.tick_mutante, self.tick_mutante)
                valor_mutante = valor + mutacao
                Populacao_ga[Individuo][p] = valor_mutante
            else:
                Populacao_ga[Individuo][p]=Populacao_ga[Individuo_mutante][p]
        #print(Individuo, Populacao_ga[Individuo])
        return Populacao_ga

    # realiza uma interação em cada posição para uma busca local do minimo
    def op_downhill(self, Individuo, Populacao_ga, modelo_referencia):


        rand = random.choice(list(Populacao_ga.keys()))
        Individuo_x = Populacao_ga[rand]
        individuo_x_keys=list(Populacao_ga[rand].keys())
        while not 'fitness' in individuo_x_keys:
            rand = random.choice(list(Populacao_ga.keys()))
            Individuo_x = Populacao_ga[rand]
            individuo_x_keys = list(Populacao_ga[rand].keys())


        fitness_x = Individuo_x['fitness']
        Individuo_beta={}
        for p in self.vetor_parametro:
            parametro = Individuo_x[p]

            # calcula a primeira alteracao positiva
            parametro_teste1 = parametro + self.vetor_parametro[p][2]
            Individuo_x[p]=parametro_teste1
            modelo_valor_teste1 = modelo_teste.modelo(self.espaco_simulacao, Individuo_x)
            fitness_teste1 = fitness.fitness(modelo_valor_teste1, modelo_referencia, self.vetor_peso)

            # calcula a primeira alteracao negativa
            parametro_teste2=parametro- self.vetor_parametro[p][2]
            Individuo_x[p]=parametro_teste2
            modelo_valor_teste2 = modelo_teste.modelo(self.espaco_simulacao, Individuo_x)
            fitness_teste2 = fitness.fitness(modelo_valor_teste2, modelo_referencia, self.vetor_peso)

            Individuo_x[p]=parametro
            if self.otimizador=='minimo':
                if fitness_teste1 < fitness_x:
                    Individuo_beta[p]= parametro_teste1
                elif fitness_teste2 <fitness_x:
                    Individuo_beta[p] = parametro_teste2
                else:
                    Individuo_beta[p] = parametro

            elif self.otimizador=='maximo':
                if fitness_teste1 > fitness_x:
                    Individuo_beta[p]= parametro_teste1
                elif fitness_teste2 > fitness_x:
                    Individuo_beta[p] = parametro_teste2
                else:
                    Individuo_beta[p] = parametro

        modelo_valor_beta = modelo_teste.modelo(self.espaco_simulacao, Individuo_beta)
        fitness_beta = fitness.fitness(modelo_valor_beta, modelo_referencia, self.vetor_peso)
        #Individuo_beta['fitness']=fitness_beta
        #keyboard.wait('esc')
        Populacao_ga[Individuo]= Individuo_beta
        Populacao_ga[Individuo]['fitness']=fitness_beta

        #keyboard.wait('esc')

        return Populacao_ga


    def op_crossover(self, Individuo, Populacao_ga):
        Lista = list(Populacao_ga.keys())

        Individuo1 = random.choice(Lista)
        Individuo2 = random.choice(Lista)
        #print(Populacao_ga[Individuo1])
        #print(Populacao_ga[Individuo2])

        Populacao_ga[Individuo] = {}
        for p in self.vetor_parametro:
            aleatorio = random.randint(0, 2)
            if aleatorio == 0:
                Populacao_ga[Individuo][p]=Populacao_ga[Individuo1][p]
            elif aleatorio == 1:
                Populacao_ga[Individuo][p] = Populacao_ga[Individuo2][p]
            elif aleatorio == 2:
                Populacao_ga[Individuo][p] = (Populacao_ga[Individuo1][p]+Populacao_ga[Individuo2][p])/2
        #print(Populacao_ga[Individuo])
        return Populacao_ga


#############################################################
    # retorna o melhor individuo da populacao (o highlander)
    def solucao_aquiles(self,Populacao_ga):
        Lista = list(Populacao_ga.keys())
        aquiles = Lista[-1]
        fitness_aquiles = Populacao_ga[aquiles]['fitness']
        if self.otimizador == 'minimo':
            for individuo in Populacao_ga:
                if Populacao_ga[individuo]['fitness'] < fitness_aquiles:
                    fitness_aquiles = Populacao_ga[individuo]['fitness']
                    aquiles= individuo
        elif self.otimizador=='maximo':
            for individuo in Populacao_ga:
                if Populacao_ga[individuo]['fitness'] > fitness_aquiles:
                    fitness_aquiles = Populacao_ga[individuo]['fitness']
                    aquiles= individuo

        config_aquiles ={}
        for p in self.parametro_modelo:
            config_aquiles[p] = Populacao_ga[aquiles][p]

        return {'aquiles':aquiles,
                'fitness':fitness_aquiles,
                'config':config_aquiles}

    #############################################################################
    # calcula o valor de fitness para os individuos sem o valor na populacao
    def calcula_fitness(self,Populacao_ga, vetor_ref):
        for i in Populacao_ga:
            individuo=Populacao_ga[i]
            if not 'fitness' in individuo.keys():
                modelo_valor = modelo_teste.modelo(self.espaco_simulacao, individuo)
                fitness_valor=fitness.fitness(modelo_valor, vetor_ref, self.vetor_peso)
                Populacao_ga[i]['fitness']=fitness_valor
        return Populacao_ga

    #############################################
    # algortimo genetico da otimização de sistemas dinamicos calibrados
    # por parametros estatisticas
    # Vetor_parametros = {p1:[X_inicio, X_final, precisao]}
    def cria_populacao_inicial(self, N_pop):
        vetor_parametro = self.vetor_parametro
        Populacao={}
        for i in range(N_pop):
            Populacao[i]={}

            for gene in vetor_parametro:
                P_inicio = vetor_parametro[gene][0]
                P_final = vetor_parametro[gene][1]
                P_valor = random.uniform(P_inicio, P_final)
                Populacao[i][gene]=P_valor
                #Populacao[i]= {'a':4.0, 'b':-2.,'c':-7.00,'d':10} #P_valor
        return Populacao

    ########################################################################
    # cria apenas um individuo aleatorio
    def cria_individuo(self):
        cromossomo={}
        vetor_parametro = self.vetor_parametro
        for gene in vetor_parametro:
            P_inicio = vetor_parametro[gene][0]
            P_final = vetor_parametro[gene][1]
            P_valor = random.uniform(P_inicio, P_final)
            cromossomo[gene]=P_valor
        return cromossomo


GA=GA_VOGA()
r=GA.ga_voga()
print(r)