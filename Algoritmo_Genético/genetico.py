from random import *
import matplotlib.pyplot as plt 
from funcoesAuxiliares import *

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
    geraYPopulcao(_populacao)
    return _populacao

# pega o valor de f(x1,x2)
def geraYPopulcao(_populacao):
    for individuo in _populacao:
        individuo['y'] = alpine2(individuo['x1'], individuo['x2'])
    rankingLinear(_populacao)

# ajusta o valor de f(x1,x2) em uma escala
def rankingLinear(_populacao):
    global escala
    # ordena o vetor de forma crescente
    mergeSort(_populacao)
    min = escala[0]
    max = escala[1]
    N = len(_populacao)
    for index in range(0, N):
        i = N - index
        y = min + ( (max - min) * (N - i) / (N - 1) )
        _populacao[index]['y'] = y

# seleciona um individuo aleatório
def roleta(total):
    global populacao
    sorteado = uniform(0, total)
    for _individuo in populacao:
        if sorteado < _individuo['somatorio']:
            return _individuo

# gera dois filhos a partir dos genes dos pais
def geraFilho(pai, mae):
    a = uniform(0,1)
    filhos = [{
            'x1': a * pai['x1'] + (1 - a) * mae['x1'],
            'x2': a * pai['x2'] + (1 - a) * mae['x2'],
        },{
            'x1': a * mae['x1'] + (1 - a) * pai['x1'],
            'x2': a * mae['x2'] + (1 - a) * pai['x2'],
        }]
    return filhos

# faz o cruzamento da população
def geraCruzamento():
    global populacao
    _nova_populacao = []
    # a aptidão de cada indivíduo F(xi) é computada em relação à soma do desempenho bruto de todos os indivíduos f(xi)
    total = 0
    for _individuo in populacao:
        total += _individuo['y']
        _individuo['somatorio'] = total
    # separa N casais, sendo N metade do tamanho da população
    for j in range(0, int(len(populacao)/2)):
        # sorteia os pais
        pai = roleta(total)
        mae = roleta(total)
        # verifica se os pais vao gerar filhos
        if uniform(0,1) < taxa_reproducao:
            # gera filhos e mata os pais (não são passados a diante)
            filhos = geraFilho(pai, mae)
            _nova_populacao.append(filhos[0])
            _nova_populacao.append(filhos[1])
        else:
            # mantem os pais
            _nova_populacao.append(pai)
            _nova_populacao.append(mae)
    
    # a nova geração pode sofrer mutações
    mutacao(_nova_populacao)
    # pega os valores de f(x1, x2)
    geraYPopulcao(_nova_populacao)
    # nova geração
    populacao = _nova_populacao

# faz mutação dos genes
def mutacao(_populacao):
    for individuo in _populacao:
        # muta gene x1
        if uniform(0,1) < taxa_mutacao:
            individuo['x1'] += uniform(-alcance_mutacao, alcance_mutacao)
            if individuo['x1'] > 10:
                individuo['x1'] = 10
            elif individuo['x1'] < 0:
                individuo['x1'] = 0
        # muta gene x2
        if uniform(0,1) < taxa_mutacao:
            individuo['x2'] += uniform(-alcance_mutacao, alcance_mutacao)
            if individuo['x2'] > 10:
                individuo['x2'] = 10
            elif individuo['x2'] < 0:
                individuo['x2'] = 0


# plota gráfico da população
def PlotaGraficoPopulacao(_geracao=0, _color='green'):
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

# plota gráfico do erro
def PlotaGraficoMedia(x1, x2, _color='green'):
    # plotar gráfico de pontos
    plt.scatter(x1, x2)  
    plt.title(f'Gráfico do Erro', color=_color) 
    plt.xlabel('x1') 
    plt.ylabel('x2') 
    plt.show() 

def genetico(show_generations = False):
    media_x1 = []
    media_x2 = []
    for geracao in range(0, geracoes+1):
        # faz o cruzamento
        geraCruzamento()
        # pega o ponto médio
        x1 = 0
        x2 = 0
        for individuo in populacao:
            x1 += individuo['x1']
            x2 += individuo['x1']
        media_x1.append(x1/len(populacao))
        media_x2.append(x2/len(populacao))
        
        # mostra gráfico de pontos
        if show_generations is True:
            if geracao % 10 == 0:
                PlotaGraficoPopulacao(geracao)
        
    # mostra progressão do ponto médio
    PlotaGraficoMedia(media_x1, media_x2)

# parametros 
escala = [0, 10]
geracoes= 100
taxa_reproducao = 0.7
taxa_mutacao = 0.1
alcance_mutacao = 1
# cria população
populacao = geraPopulacao(100)
# excuta o algoritmo
genetico()