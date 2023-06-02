from re import X


class Formiga():
    def __init__(self, partida, x, y, cidade, lst_cidades) -> None:
        self.partida = partida
        self.x = x
        self.y = y
        self.cidade = cidade
        self.lst_cidades_a_visitar = lst_cidades
