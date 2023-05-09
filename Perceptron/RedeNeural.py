# João Victor Dias Gomes
# Ana Júlia Rodrigues

from neuronio import neuronio
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# le arquivo CSV
def leArquivoCSV(file):
    lst_from_csv = []
    with open(file,'r') as file:
        # ignora cabeçalho
        file.readline()
        # le as linhas do arquivo
        for linha in file:
            linha = linha.split(",")
            line_from_csv = [
                float(linha[0]),
                float(linha[1]),
                float(linha[2]),
                float(linha[3]),
                linha[4].split("\n")[0]
            ]  
            lst_from_csv.append(line_from_csv)
    file.close()
    return lst_from_csv

def sigmoidalVetor(vetor):
    if vetor[0] > vetor[1] and vetor[0] > vetor[2]:
        vetor = [1, 0, 0]
    elif vetor[1] > vetor[2]:
        vetor = [0, 1, 0]
    else:
        vetor = [0, 0, 1]
    return vetor

def redeNeural(epoca_max, funcao = 0, learning_rate=0.1):
    # declara erro total
    Erro_total = []

    # declara os 3 neuronios
    n1 = neuronio(funcao, learning_rate)
    n2 = neuronio(funcao, learning_rate)
    n3 = neuronio(funcao, learning_rate)

    """     TREINO   """
    epoca = 0
    while epoca < epoca_max:
        # declara erro da epoca
        Erro_epoca = 0
        for i, x in enumerate(X_treino):
            # resposta esperada
            species = y_treino[i]

            # passa a entrada para os neuronios
            y = [0,0,0]
            y[0] = n1.fit(x)
            y[1] = n2.fit(x)
            y[2] = n3.fit(x)

            # calculo do erro
            erro1 = d[species][0] - y[0]
            erro2 = d[species][1] - y[1]
            erro3 = d[species][2] - y[2]
            Erro_epoca += (erro1*erro1)+(erro2*erro2)+(erro3*erro3)

            # atualiza os pesos e os bias de cada neuronio
            n1.atualiza(x, erro1)
            n2.atualiza(x, erro2)
            n3.atualiza(x, erro3)
        # adiciona o erro da epoca 
        Erro_total.append(Erro_epoca)
        # proxima epoca
        epoca += 1

    """     TESTE    """
    acerto = 0
    for i, x in enumerate(X_teste):
        # resposta esperada
        species = y_teste[i]
        # passa a entrada pelos neuronios
        y = [0,0,0]
        y[0] = n1.fit(x)
        y[1] = n2.fit(x)
        y[2] = n3.fit(x)
        # avalia resposta
        if funcao == 0:
            if d[species] == y:
                acerto += 1
        else:
            if d[species] == sigmoidalVetor(y):
                acerto += 1
    # mostra o resultado do teste
    if funcao == 0:
        print(f"Acurácia Degrau: {round((acerto/len(y_teste))*100, 1)}%")
    else:
        print(f"Acurácia Sigmoidal: {round((acerto/len(y_teste))*100,1)}%")
    print("=============================")

    """  PLOTA OS GRÁFICOS DOS ERROS   """
    if funcao == 0:
        plt.title('Gráfico do erro com função Degrau')
    else:
        plt.title('Gráfico do erro com função Sigmoidal')
    plt.plot(list(range(len(Erro_total))), Erro_total, 'tab:red')
    plt.show()
    

# Recebe os dados do arquivo csv
iris = leArquivoCSV("Iris_Data.csv")

# Modelo da resposta
d = {
    "Iris-setosa": [1, 0, 0],
    "Iris-versicolor": [0, 1, 0],
    "Iris-virginica": [0, 0, 1]
}

# determina a quantidade de epocas do treino
qtd_epocas = 100

# separa os dados em teste e terino
X = []
y = []
for element in iris:
    X.append(element[0:4])
    y.append(element[4])
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=42)
print("=============================")
print(f"TOTAL DE AMOSTRAS: {len(X)}")
print(f"Treino: {len(X_treino)} Teste: {len(X_teste)}")
print(f"ÉPOCAS: {qtd_epocas}")
print("=============================")

# rede usando função degrau
redeNeural(qtd_epocas, 0)

# rede usando função sigmoidla
redeNeural(qtd_epocas, 1)

