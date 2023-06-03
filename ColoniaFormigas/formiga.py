class Formiga():
    def __init__(self, partida, x, y, lst_cidades) -> None:
        self.partida = partida
        self.x = x
        self.y = y
        self.cidade = partida
        self.lst_cidades_a_visitar = lst_cidades
        self.caminho = [partida]
        self.custo = 0

    def imprimir(self):
        print(f"Partida: {self.partida} (x: {self.x}, y:{self.y}) Atualmente: {self.cidade}")
        print(f"Ainda a visitar: {self.lst_cidades_a_visitar}")
        print(f"Caminho: {self.caminho}")
        print(f"Custo: {round(self.custo, 2)}")
        print("---------------------------------------")
