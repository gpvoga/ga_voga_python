

from statistics import mean, stdev

# modelo teste para versao ga voga doutorado

def modelo(x_espaco_simulacao, individuo):
    x_inicio = x_espaco_simulacao['xi']
    x_final = x_espaco_simulacao['xf']
    x_passo = x_espaco_simulacao['passo']

    a=individuo['a']
    b=individuo['b']
    c=individuo['c']
    d=individuo['d']

    x_lista = []
    y_lista = []
    dy_lista =[]
    d2y_lista=[]
    N_passo = int((x_final - x_inicio)//x_passo + 1)
    cont = 0
    for cont in range(N_passo):
        xi = x_inicio+cont*x_passo
        yi = a*(xi**3)+b*(xi**2)+c*(xi**1)+d
        dyi = 3*a*(xi**2)+2*b*(xi**1)+c
        d2yi = 2*3*a*(xi**1)+2*b*(xi)

        x_lista.append(xi)
        y_lista.append(yi)
        dy_lista.append(dyi)
        d2y_lista.append(d2yi)

    y_media = mean(y_lista)
    dy_media = mean(dy_lista)
    d2y_media = mean(d2y_lista)

    y_desvio = stdev(y_lista)
    dy_desvio = stdev(dy_lista)
    d2y_desvio = stdev(d2y_lista)

    return {'y_media':y_media,
            'y_desvio':y_desvio,
            'dy_media':dy_media,
            'dy_desvio':dy_desvio,
            'd2y_media':d2y_media,
            'd2y_desvio':d2y_desvio}