import matplotlib.pyplot as plt
import numpy as np
import math
import random

# plota gráficos
def plota_graficos(_eixo_x, _graficos, _msg):
    plt.title(f"Gráfico {_msg['titulo']}")
    plt.xlabel(_msg["eixo_x"], fontsize=15)
    plt.ylabel(_msg["eixo_y"], fontsize=15)
    for _grafico in _graficos:
        plt.plot(_eixo_x, _grafico["dado"], "tab:"+_grafico["cor"])
    plt.legend(_msg["legenda"])
    plt.show()

if __name__ == "__main__":
    # inputs e outputs
    universo = []
    curva_funcao = []
    curva_estimada = []
    erro_epocas = []
    gaussiana_1 = []
    gaussiana_2 = []

    # parâmetros
    num_epocas = 100
    epoca = 0
    p1 = 2
    p2 = -2
    q1 = 1
    q2 = -1
    x1 = 2
    x2 = -2
    sigma1 = 1 # desvio padrão
    sigma2 = 1 # desvio padrão
    alfa = 0.1

    # cria o universo e a parabola x^2
    for num in np.linspace(-2, 2.0, 100, True):
        universo.append(num)
        curva_funcao.append( pow(num, 2) )
        gaussiana_1.append( math.exp(-0.5 * math.pow( (num - x1) / sigma1 ,2)) )
        gaussiana_2.append( math.exp(-0.5 * math.pow( (num - x2) / sigma2 ,2)) )

    # treina o modelo
    while epoca < num_epocas:
        universo_random  = random.sample(universo, len(universo))
        erro_total = 0

        for x in universo_random:
            # calcula os parametros
            y1 = p1 * x + q1
            y2 = p2 * x + q2
            w1 = math.exp(-0.5 * math.pow( (x - x1) / sigma1 ,2))
            w2 = math.exp(-0.5 * math.pow( (x - x2) / sigma2 ,2))
            y = ((w1 * y1) + (w2 * y2)) / (w1+w2)

            # calcula o erro
            erro = y - pow(x, 2) # y - yd
            erro_p1 = erro * (w1 / (w1+w2)) * x
            erro_p2 = erro * (w2 / (w1+w2)) * x
            erro_q1 = erro * (w1 / (w1+w2))
            erro_q2 = erro * (w2 / (w1+w2))
            erro_x1 = erro * w2 * ( (y1 - y2) / pow(w1+w2, 2) ) * w1 * ( (x - x1) / pow(sigma1,2) )
            erro_x2 = erro * w1 * ( (y2 - y1) / pow(w1+w2, 2) ) * w2 * ( (x - x2) / pow(sigma2,2) )
            erro_sigma1 = erro * w2 * ( (y1 - y2) / pow(w1+w2, 2) ) * w1 * ( pow(x - x1, 2) / pow(sigma1,3) )
            erro_sigma2 = erro * w1 * ( (y2 - y1) / pow(w1+w2, 2) ) * w2 * ( pow(x - x2, 2) / pow(sigma2,3) )
            erro_total += erro_p1 + erro_p2 + erro_q1 + erro_q2 + erro_x1 + erro_x2 + erro_sigma1 + erro_sigma2
            
            # Ajusta os parametros
            p1 = p1 - (alfa * erro_p1)
            p2 = p2 - (alfa * erro_p2)
            q1 = q1 - (alfa * erro_q1)
            q2 = q2 - (alfa * erro_q2)
            x1 = x1 - (alfa * erro_x1)
            x2 = x2 - (alfa * erro_x2)
            sigma1 = sigma1 - (alfa * erro_sigma1)
            sigma2 = sigma2 - (alfa * erro_sigma2)

        # ajusta o coeficiente do erro
        if epoca % 10 == 0:
            alfa -= ( 0.1 * alfa )

        # proxima epoca
        erro_epocas.append(pow(erro_total, 2))
        epoca += 1

    # gera a curva estimada
    erro_curva = 0
    for x in universo:
        y1 = p1 * x + q1
        y2 = p2 * x + q2
        w1 = math.exp(-0.5 * math.pow( (x - x1) / sigma1 ,2))
        w2 = math.exp(-0.5 * math.pow( (x - x2) / sigma2 ,2))
        y = ((w1 * y1) + (w2 * y2)) / (w1+w2)
        curva_estimada.append(y)

        # calcula o erro
        erro = y - pow(x, 2) # y - yd
        erro_p1 = erro * (w1 / (w1+w2)) * x
        erro_p2 = erro * (w2 / (w1+w2)) * x
        erro_q1 = erro * (w1 / (w1+w2))
        erro_q2 = erro * (w2 / (w1+w2))
        erro_x1 = erro * w2 * ( (y1 - y2) / pow(w1+w2, 2) ) * w1 * ( (x - x1) / pow(sigma1,2) )
        erro_x2 = erro * w1 * ( (y2 - y1) / pow(w1+w2, 2) ) * w2 * ( (x - x2) / pow(sigma2,2) )
        erro_sigma1 = erro * w2 * ( (y1 - y2) / pow(w1+w2, 2) ) * w1 * ( pow(x - x1, 2) / pow(sigma1,3) )
        erro_sigma2 = erro * w1 * ( (y2 - y1) / pow(w1+w2, 2) ) * w2 * ( pow(x - x2, 2) / pow(sigma2,3) )
        erro_curva += erro_p1 + erro_p2 + erro_q1 + erro_q2 + erro_x1 + erro_x2 + erro_sigma1 + erro_sigma2
    erro_curva = pow(erro_curva, 2)
    # plota os gráficos
    grafico = [
        {"dado": curva_funcao, "cor": "green"},
        {"dado": gaussiana_1, "cor": "cyan"},
        {"dado": gaussiana_2, "cor": "blue"},
        {"dado": curva_estimada, "cor": "red"},
    ]
    msg = {
        "eixo_x": "x",
        "eixo_y": "y",
        "titulo": "Gráfico modelo fuzzy", 
        "legenda": [
            "Parabola x^2",
            "Gaussiana 01",
            "Gaussiana 02",
            "Curva Estimada"
        ]
    }
    plota_graficos(universo, grafico, msg)
    grafico = [
        {"dado": erro_epocas, "cor": "blue"},
    ]
    msg = {
        "eixo_x": "Epocas",
        "eixo_y": "Erro",
        "titulo": "Curva do erro", 
        "legenda": ["Erro final: " +str(round(erro_curva, 3))]
    }
    plota_graficos(range(1, len(erro_epocas)+1), grafico, msg)
