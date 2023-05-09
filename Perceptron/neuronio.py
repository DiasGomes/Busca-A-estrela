from random import random
from math import exp

class neuronio():
    def __init__(self, funcao = 0, learning_rate=0.1) -> None:
        # inicializa os pesos e o bias com valores aleatórios
        self.w = [(random() * 2) - 1,(random() * 2) - 1,(random() * 2) - 1,(random() * 2) - 1]
        self.bias = (random() * 2) - 1
        self.learning_rate = learning_rate
        self.funcao = funcao

    def imprimir(self):
        print(f"W: {self.w}\nBias: {self.bias}")

    def fit(self, x):
        u = self.calculoU(x)
        if self.funcao == 0:
            y = degrau(u)
        else:
            y = sigmoidal(u)
        return y
        
    def atualiza(self, x, erro):
        # atualiza os pesos
        for i in range(len(self.w)):
            self.w[i] = self.w[i] + ((erro * self.learning_rate) * x[i])
        # atualiza o bias
        self.bias = self.bias + (erro * self.learning_rate)

    # calcula o valor de u
    def calculoU(self, entrada):
        u = 0
        for i, x in enumerate(entrada):
            u = u + (self.w[i] * x)
        return u + self.bias

# função degrau
def degrau(x):
    return 1 if x >= 0 else 0

def sigmoidal(x):
    return 1 / ( 1 + exp(-x) )

