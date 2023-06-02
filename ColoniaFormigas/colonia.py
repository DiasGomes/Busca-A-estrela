import math
from formiga import Formiga
#import matplotlib.pyplot as plt 

# le o arquibvo CSV
def leArquivo(file):
    with open(file,'r') as file:
        cabecalho = file.readline()
        # abre o arquivo de grafo
        conteudo = []
        for linha in file:
            conteudo.append({
                cabecalho.split(";")[0].split("¿")[1]: linha.split(";")[0],
                cabecalho.split(";")[1]: float(linha.split(';')[1]),
                cabecalho.split(";")[2].split("\n")[0]: float(linha.split(';')[2].split("\n")[0]),
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
    plt.xlabel('Geração') 
    plt.ylabel('Fitness') 
    plt.show() 

# coloca feromonio em todos os caminhos no inicio
def geraRotas():
    lst_caminhos = []
    for x in range(1,33):
        for y in range(1,33):
            distancia = calculoVizinhanca(x, y)
            lst_caminhos.append({
                "origem": x,
                "destino": y,
                "distancia": distancia,
                "feromonio": 1
            })

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
def imprimiFormigas():
    for formiga in lst_formigas:
        print(f"Partida: {formiga.partida} (x: {formiga.x}, y:{formiga.y}) Atualmente: {formiga.cidade}")
        print(f"Ainda a visitar: {formiga.lst_cidades_a_visitar}")
        print("---------------------------------------")

# gera as formigas e todas as cidades
def criaFormigas():
    for i, city in enumerate(mapa):
        lst_caminho = mapa.copy()
        del lst_caminho[i]
        lst_formigas.append(
            Formiga(city["Cidade"], city["X"], city["Y"], city["Cidade"], lst_caminho)
        )

# Probabilidade de Transição
def probabilidade():
    # percorre cada formiga
    for origem, formiga in enumerate(lst_formigas):
        total = 0
        for destino in formiga.lst_cidades_a_visitar:
            total += caminhos[origem][destino]
        print(total)
        """
        probabilidade = []
        for caminho in caminhos:
            probabilidade.append(math.pow() * math.pow() / total)
        """

def colonia():
    for iteracao in range(1, iteracoes+1):
        probabilidade()

# instancia variaveis de controle
alfa = 1
beta = 1
iteracoes = 20
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

# mostra as formigas
#imprimiFormigas()

# grafico com a distancia media, min e max
#plotaGrafico()
# rota total: 58.8