# gera um relatorio basico (json) para descrição do comportamento estatistico de um conjunto em relacao
# a media ou a uma funcao de ajuste medio

from statistics import *
import csv
from datetime import date, datetime
from database_acess import db_execute

    ################################################################################################
    #
    # faz o calculo do vetor ananlise estatistica completa para um vetor de dados
    # vetor_teste = [2, 5, 6.9, 4, 1, 9, 5, 9, 2, 6.1, 6.9, 9, 4, 3, 5, 7, 9, 9, 9, 9, 9, 9, 9]
    # r= estatistica_descritiva(vetor_teste)
    #
    #################################################################################################

def estatistica_descritiva(vetor):
        n = len(vetor)
        n_passo = 100
        # calculo da distribuicao
        distribuicao_vetor = distribuicao(vetor, n_passo)

        # calculo da media
        media = mean(vetor)

        # calculo da mediana
        maximo = max(vetor)
        minimo = min(vetor)
        mediana = (maximo + minimo) / 2

        # calculo da moda
        moda_vetor = moda(distribuicao_vetor)
        moda_valor = moda_vetor['moda']
        moda_frequencia = moda_vetor['frequencia']

        # caloculo da mediadas de dispercao
        desvio = stdev(vetor)
        assimetria_valor = assimetria(vetor, media, desvio)
        curtose_valor = curtose(vetor, media, desvio)

        # calculo da extratificacao da media (acime e baixo )
        Up_Down = separa_up_down(vetor, media)
        Up_lista = Up_Down['up']
        Down_lista = Up_Down['down']
        frequencia_up = len(Up_lista) / n

        frequencia_down = len(Down_lista) / n

        media_up = mean(Up_lista)
        desvio_up = stdev(Up_lista)

        media_down = mean(Down_lista)
        desvio_down = stdev(Down_lista)

        # caculo do sharpe
        if desvio == 0.0:
            sharpe = 0.0
        else:
            sharpe = media / desvio

        return {  # 'distribuicao':distribuicao_vetor,
            'media': media,  # ok
            'mediana': mediana,  # ok
            'moda': moda_valor,  # ok
            'moda_frequencia': moda_frequencia,  # ok
            'media_max': media_up,
            'media_min': media_down,
            'frequencia_up': frequencia_up,
            'frequencia_down': frequencia_down,
            'desvio_up': desvio_up,
            'desvio_down': desvio_down,
            'desvio': desvio,
            'assimetria': assimetria_valor,
            'curtose': curtose_valor,
            'sharpe': sharpe}

    #####################################################################################
    #                                                                                   #
    # calculo individual de cada propriedade estatistica                                #
    # das propriedades media, mediana, moda, media_up media_down                        #
    # nome ={media, mediana, moda, media_up, media_down, media_up_dow,                  #
    #        desvio, assimetria, curtose, sharpe}                                       #
    #                                                                                   #
    #####################################################################################

def estatistica_descritiva_propriedade(vetor, nome):
        n = len(vetor)

        # calculo da media
        if nome=='media':
            valor = mean(vetor)

        # calculo da mediana
        elif nome=='mediana':
            maximo = max(vetor)
            minimo = min(vetor)
            valor = (maximo + minimo) / 2

        # calculo da moda
        elif nome == 'moda':
            n_passo = 100
            # calculo da distribuicao
            distribuicao_vetor = distribuicao(vetor, n_passo)
            moda_vetor = moda(distribuicao_vetor)
            valor = moda_vetor['moda']

        # calculo da extratificacao da media (acime e baixo )
        elif nome == 'media_max':
            media = mean(vetor)
            Up_Down = separa_up_down(vetor, media)
            Up_lista = Up_Down['up']
            valor = mean(Up_lista)

        elif nome == 'media_min':
            media = mean(vetor)
            Up_Down = separa_up_down(vetor, media)
            Down_lista = Up_Down['down']
            valor = mean(Down_lista)

        elif nome == 'media_up_down':
            media = mean(vetor)
            Up_Down = separa_up_down(vetor, media)
            Up_lista = Up_Down['up']
            Down_lista = Up_Down['down']

            media_up = mean(Up_lista)
            media_down = mean(Down_lista)
            valor = {'media_max':media_up, 'media_min':media_down}

        # calculo da mediadas de dispercao DESVIO
        elif nome=='desvio':
            valor = stdev(vetor)

        # calculo da mediadas de dispercao ASSIMETRIA
        elif nome=='assimetria':
            media = mean(vetor)
            desvio = stdev(vetor)
            valor = assimetria(vetor, media, desvio)

        # calculo da mediadas de dispercao CURTOSE
        elif nome=='curtose':
            media = mean(vetor)
            desvio = stdev(vetor)
            valor = curtose(vetor, media, desvio)

        # caculo do sharpe
        elif nome=='sharpe':
            media = mean(vetor)
            desvio = stdev(vetor)
            if desvio == 0.0:
                valor = 0.0
            else:
                sharpe = media / desvio

        return {nome: valor}


    #####################################################################################
    #                                                                                   #
    # calculo individual de cada propriedade estatistica                                #
    # das propriedades media, mediana, moda, media_up media_down                        #
    # nome ={media, mediana, moda, media_up, media_down, media_up_dow,                  #
    #        desvio, assimetria, curtose, sharpe}                                       #
    #                                                                                   #
    #####################################################################################

def estatistica_descritiva_propriedade_lista(vetor, nome_lista):
        n = len(vetor)
        valor ={}
        for nome in nome_lista:
            nome= str(nome)
            # calculo da media
            if nome=='media':
                valor[nome] = mean(vetor)

            # calculo da mediana
            elif nome=='mediana':
                maximo = max(vetor)
                minimo = min(vetor)
                valor[nome] = (maximo + minimo) / 2

            # calculo da moda
            elif nome == 'moda':
                n_passo = 100
                # calculo da distribuicao
                distribuicao_vetor = distribuicao(vetor, n_passo)
                moda_vetor = moda(distribuicao_vetor)
                valor[nome] = moda_vetor['moda']

            # calculo da extratificacao da media (acime e baixo )
            elif nome == 'media_max':
                media = mean(vetor)
                Up_Down = separa_up_down(vetor, media)
                Up_lista = Up_Down['up']
                valor[nome] = mean(Up_lista)

            elif nome == 'media_min':
                media = mean(vetor)
                Up_Down = separa_up_down(vetor, media)
                Down_lista = Up_Down['down']
                valor[nome] = mean(Down_lista)

            # calculo da mediadas de dispercao DESVIO
            elif nome=='desvio':
                valor[nome] = stdev(vetor)

            # calculo da mediadas de dispercao ASSIMETRIA
            elif nome=='assimetria':
                media = mean(vetor)
                desvio = stdev(vetor)
                valor[nome] = assimetria(vetor, media, desvio)

            # calculo da mediadas de dispercao CURTOSE
            elif nome=='curtose':
                media = mean(vetor)
                desvio = stdev(vetor)
                valor[nome] = curtose(vetor, media, desvio)

            # caculo do sharpe
            elif nome=='sharpe':
                media = mean(vetor)
                desvio = stdev(vetor)
                if desvio == 0.0:
                    valor[nome] = 0.0
                else:
                    valor[nome] = media / desvio

        return valor


    #####################################################################################
    #
    # calcula as propriedades de valores medios para calculo de tunel de disperssao
    # media, mediana, moda, media_up, media_down

    #####################################################################################

def estatistica_descritiva_media4(vetor, centro='media'):
        n = len(vetor)
        n_passo = 100
        # calculo da distribuicao
        distribuicao_vetor = distribuicao(vetor, n_passo)

        # calculo da media
        media = mean(vetor)

        # calculo da mediana
        maximo = max(vetor)
        minimo = min(vetor)
        mediana = (maximo + minimo) / 2

        # calculo da moda
        moda_vetor = moda(distribuicao_vetor)
        moda = moda_vetor['moda']

        # define a media central usada como referencia de extratificacao
        if centro=='media':
            centroide = media
        elif centro == 'moda':
            centroide = moda
        elif centro == 'mediana':
            centroide = mediana
        else:
            centroide = media

        # calculo da extratificacao da media (acime e baixo )
        Up_Down = separa_up_down(vetor, centroide)
        Up_lista = Up_Down['up']
        Down_lista = Up_Down['down']

        media_up = mean(Up_lista)
        media_down = mean(Down_lista)

        return {'centro': nome,
                'media': media,  # ok
                'mediana': mediana,  # ok
                'moda': moda,  # ok
                'media_max': media_up,
                'media_min': media_down}



    ###################################################################################
    #
    # estrutura o dicionario de distribuicao estatistica do vetor
    # ex distribuicao={0:{'n':Int, 'frequencia':float, 'media':float, 'desvio':float
    #
    ###################################################################################
def distribuicao(vetor, n_faixa):
        minimo = min(vetor)
        maximo = max(vetor)
        passo = (maximo - minimo) / n_faixa  # define o passo da distribuição
        contador_vetor = len(vetor)

        # constroi dicionario de faixas com os elementos do vetor
        # ex ditribuicao_lista = {0:[v1, v2, ...], 1:[v10, v11, ...]}
        distribuicao_lista_random = {}

        for v in vetor:
            i = int((v - minimo) / passo)
            if i in distribuicao_lista_random:
                distribuicao_lista_random[i].append(v)
            else:
                distribuicao_lista_random[i] = [v]

        # agrupa os passos unitarios com o vizinho mais proximo
        key_orden = sorted(distribuicao_lista_random)
        distribuicao_lista_ordem = []
        distribuicao_lista = {}
        for k in key_orden:
            n1 = len(distribuicao_lista_random[k])
            n_acu = len(distribuicao_lista_ordem)
            if n_acu >= 3 and n1 == 1:
                distribuicao_lista[k] = distribuicao_lista_random[k] + distribuicao_lista_ordem
                distribuicao_lista_ordem = []
            elif n1 == 1:
                distribuicao_lista_ordem = distribuicao_lista_ordem + distribuicao_lista_random[k]
            else:
                distribuicao_lista[k] = distribuicao_lista_random[k] + distribuicao_lista_ordem
                distribuicao_lista_ordem = []

        n_acu = len(distribuicao_lista_ordem)
        if n_acu >= 1:
            distribuicao_lista[k] = distribuicao_lista_ordem

        # calcula os valores da  distribuicao (tamanho, frequencia, media, desvio)
        distribuicao = {}
        key = 0
        freq_acu = 0
        for m in distribuicao_lista:
            lista_k = distribuicao_lista[m]
            contador = len(lista_k)
            # erro de divisao/0
            frequencia = float(contador / contador_vetor)
            freq_acu = freq_acu+frequencia
            media = float(mean(lista_k))
            tamanho = len(lista_k)
            if tamanho == 1:
                desvio = 0.0
            else:
                desvio = float(stdev(lista_k))
            distribuicao[key] = {'n': contador,
                                 'frequencia': frequencia,
                                 'frequencia_acu':freq_acu,
                                 'media': media,
                                 'desvio': desvio}
            key = key + 1

        return distribuicao


    ##########################################################################
    #
    # obtem o valor da moda a partir do vetor distribuicao
    # retorno {'moda':float, 'frequencia':float}
    #
    ##########################################################################

def moda(distribuicao):
        frequencia_moda = distribuicao[0]['frequencia']
        k_moda = 0
        # encontra o passo da dsitribuicao com maior frequencia
        for k in distribuicao:
            if distribuicao[k]['frequencia'] > frequencia_moda:
                k_moda = k
        valor_moda = distribuicao[k_moda]['media']
        return {'moda': valor_moda, 'frequencia': frequencia_moda}


    ######################################################################
    #
    #  Calculo da assimetria de um vetor
    # assimetria(Vetor, Media, Desvio) = assimetria_valor
    # curtose(Vetor, Media, Desvio)= curtose_valor
    # assimetria_curtose(Vetor, Media, Desvio)
    #
    ######################################################################

def assimetria(vetor, media, desvio):
        n = len(vetor)
        soma_momento = 0.0
        for v in vetor:
            soma_momento = soma_momento + (v - media) ** 3
        if desvio == 0.0:
            assimetria = 0.0
        elif n == 1:
            assimetria = 0.0
        else:
            assimetria = soma_momento / ((n - 1) * (desvio ** 3))

        return assimetria


def curtose(vetor, media, desvio):
        n = len(vetor)
        soma_momento = 0.0
        for v in vetor:
            soma_momento = soma_momento + (v - media) ** 4
        if desvio == 0.0:
            curtose = 0.0
        elif n == 1:
            curtose = 0.0
        else:
            curtose = soma_momento / ((n - 1) * (desvio ** 3))
        return curtose


def assimetria_curtose(vetor, media, desvio):
        n = len(vetor)
        soma_momento3 = 0.0
        soma_momento4 = 0.0
        for v in vetor:
            soma_momento3 = soma_momento3 + (v - media) ** 3
            soma_momento4 = soma_momento4 + (v - media) ** 4
        if desvio == 0.0:
            assimetria = 0.0
            curtose = 0.0
        elif n == 1:
            assimetria = 0.0
            curtose = 0.0
        else:
            assimetria = soma_momento3 / ((n - 1) * (desvio ** 3))
            curtose = soma_momento4 / ((n - 1) * (desvio ** 4))
        return {'assimetria': assimetria, 'curtose': curtose}


    ###############################################################################
    #
    # faz a separacao dos dados de caodo com uma media central (media, moda etc
    #
    #################################################################################

def separa_up_down(vetor, media):
        up_lista = []
        down_lista = []
        for v in vetor:
            if v >= media:
                up_lista.append(v)

            if v <= media:
                down_lista.append(v)
        return {'up': up_lista, 'down': down_lista}

#############################################################
# chamadas de teste

#r= DataHub()
#p = DataHub().estatistica_comparacao_media(888, 'media')
#p = DataHub().leitura_cliente_db(8)
#p2 = DataHub().leitura_cliente(8)
#print(p)
#print(p2)

# vetor_teste = [7927.76, 6267.6, 2148.04, 7300.85, 7128.45, 7031.96, 7780.44, 13148.5, 3532.22, 1285.03, 9889.19, 6746.22, 5212.85, 9932.23, 7683.67, 4517.04, 4968.81, 5535.03, 9895.51, 13589.89, 11657.2, 12266.05, 16999.4, 13197.38, 5158.84, 3239.87, 5598.92, 4935.0, 4812.2, 3228.67, 3717.81]
#vetor_teste= [2, 5, 6.9, 4, 1, 9, 5, 9, 2, 6.1, 6.9, 9, 4, 3, 5, 7, 9, 9, 9, 9, 9, 9, 9]
# vetor_teste=[10, 12.0, 13, 11, 11]
#r= DataHub
#p=r.estatistica_descritiva(vetor_teste)
#print(r)


#####  comando de teste das estatistica descritiva
# vetor_teste= [2, 5, 6.9, 4, 1, 9, 5, 9, 2, 6.1, 6.9, 9, 4, 3, 5, 7, 9, 9, 9, 9, 9, 9, 9]
# r= estatistica_descritiva(vetor_teste)
# print(r)

