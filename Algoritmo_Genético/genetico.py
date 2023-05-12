from random import uniform
import matplotlib.pyplot as plt 
import math

# função alpine 2
def alpine2(x1, x2):
    return math.sqrt(x1) * math.sin(x1) * math.sqrt(x2) * math.sin(x2)

# sorteia um número entre 0 e um valor
def roleta(max):
    return uniform(0,max)

# gera individuos aleatórios
def geraPopulacao(tamanho_populacao):
    _populacao = []
    count = 0
    while(count < tamanho_populacao):
        # gera números aleatorios entre 0 a 10 para x1 e x2
        _populacao.append({
            'x1': uniform(0,10),
            'x2': uniform(0,10),
        })
        count += 1
    return _populacao

# plota gráfico da população
def PloteGrafico(_geracao=0,_color='green'):
    x1 = []
    x2 = []
    for individuo in populacao:
        x1.append(individuo['x1'])
        x2.append(individuo['x2'])

    # plotar gráfico de pontos
    plt.scatter(x1, x2) 
    plt.title(f'Geração: {_geracao}', color=_color) 
    plt.xlabel('x1') 
    plt.ylabel('x2') 
    plt.show() 

populacao = geraPopulacao(100)
PloteGrafico()
for individuo in populacao:
    resultado = alpine2(individuo['x1'], individuo['x2'])
    print(resultado)



