import math
from formiga import Formiga
import matplotlib.pyplot as plt 
from random import uniform

# le o arquibvo CSV
def leArquivo(file):
    with open(file,'r') as file:
        cabecalho = file.readline()
        # abre o arquivo de grafo
        conteudo = []
        for linha in file:
            conteudo.append({
                cabecalho.split(";")[0].split("¿")[1]: linha.split(";")[0], # Cidade
                cabecalho.split(";")[1]: float(linha.split(';')[1]), # X
                cabecalho.split(";")[2].split("\n")[0]: float(linha.split(';')[2].split("\n")[0]), # Y
            })
        file.close()
        return conteudo

# plota gráfico do erro
def plotaGrafico(lst_iteracoes, max, min, media):
    # plotar gráfico de pontos
    plt.plot(lst_iteracoes, max, color='green') 
    plt.plot(lst_iteracoes, min, color='red') 
    plt.plot(lst_iteracoes, media, color='blue') 
    plt.title(f'Gráfico da Média') 
    plt.xlabel('Iteração') 
    plt.ylabel('Fitness') 
    plt.show() 

# coloca feromonio em todos os caminhos no inicio
def geraRotas():
    lst_caminhos = []
    for x in range(1,33):
        linha = []
        for y in range(1,33):
            distancia = calculoVizinhanca(x, y)
            linha.append({
                "origem": x,
                "destino": y,
                "distancia": distancia,
                "feromonio": 1
            })
        lst_caminhos.append(linha)

    return lst_caminhos

# calcula a disntancia em linha reta das cidades
def calculoVizinhanca(city1, city2):
    global mapa
    # como esta ordenado basta pegar a posição do vetor
    ponto1 = mapa[city1 - 1]
    ponto2 = mapa[city2 - 1]
    _x = ponto1["X"] - ponto2["X"]
    _y = ponto1["Y"] - ponto2["Y"]
    distancia = math.sqrt(math.pow(_x,2) + math.pow(_y,2))
    return distancia

# impirimi as formigas
def imprimiFormigas(option=0):
    if option == 0:
        for formiga in lst_formigas:
            formiga.imprimir()
    else:
        lst_formigas[option-1].imprimir()
        
# seleciona um individuo aleatório
def roleta(prob_rotas, total):
    sorteado = uniform(0, total)
    for prob_rota in prob_rotas:
        if sorteado < prob_rota['somatorio']:
            return prob_rota['destino']

# gera as formigas e todas as cidades
def criaFormigas():
    for i, city in enumerate(mapa):
        # lista de todas as cidades menos a que ela começa
        lst_caminho = mapa.copy()
        del lst_caminho[i]
        # cria formiga (onde inciou, x, y, cidade atual, lista de cidades a visitar)
        lst_formigas.append(
            Formiga(city["Cidade"], city["X"], city["Y"], lst_caminho)
        )

# Probabilidade de Transição
def probabilidade():
    # percorre cada formiga
    for origem, formiga in enumerate(lst_formigas):
        # calcula o total e o custo das rotas que devem ser visitadas
        total = 0
        probabilidade = []
        for i, destino in enumerate(formiga.lst_cidades_a_visitar):
            feromonio = math.pow(caminhos[origem][int(destino["Cidade"])-1]["feromonio"], alfa)
            distancia = math.pow(caminhos[origem][int(destino["Cidade"])-1]["distancia"], beta)
            resultado = feromonio * distancia
            total += resultado
            if i > 0:
                resultado += probabilidade[i-1]["somatorio"]
            probabilidade.append({
                "somatorio": resultado,
                "destino": destino["Cidade"],
            })

        # determina para onde a formiga vai
        nova_cidade = roleta(probabilidade, total)
        # formiga vai para proxima cidade

        for destino in formiga.lst_cidades_a_visitar:
            # atualiza informações da formiga
            if destino["Cidade"] == nova_cidade:
                formiga.cidade = nova_cidade
                formiga.x = destino["X"] 
                formiga.y = destino["Y"]
                formiga.lst_cidades_a_visitar.remove(destino)
                formiga.caminho.append(nova_cidade)
                formiga.custo += caminhos[origem][int(destino["Cidade"])-1]["distancia"] 
                break

# algoritmo de colonia
def colonia():
    lst_iteracoes = []
    lst_media = []
    lst_max = []
    lst_min = []
    iteracao = 0
    while iteracao < iteracoes:
        cidades_visitadas = 1
        while cidades_visitadas < len(mapa) + 1:
            probabilidade()
            cidades_visitadas += 1
        
        max = None
        min = None
        media = 0
        for formiga in lst_formigas:
            media += formiga.custo
            if max is None or max < formiga.custo:
                max = formiga.custo
            if min is None or min > formiga.custo:
                min = formiga.custo
        lst_max.append(max)
        lst_min.append(min)
        lst_media.append(media/( len(lst_formigas) + 1 )) 
        lst_iteracoes.append(iteracao)
        iteracao += 1

    plotaGrafico(lst_iteracoes, lst_max, lst_min, lst_media)

# instancia variaveis de controle
alfa = 1
beta = 1
iteracoes = 100
evaporacao = 0.5

# le o arquivo csv e instancia o mapa das cidades
mapa = leArquivo("Colonia.csv")

# instancia matriz dos caminhos
caminhos = geraRotas()

# instancia as formigas
lst_formigas = []
criaFormigas()

# executa as iterações
colonia()
# rota total: 58.8