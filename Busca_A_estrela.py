# João Victor Dias Gomes
# Ana Júlia Rodrigues

def leArquivo(file, opcao=0):
    with open(file,'r') as file:
        # abre o arquivo de grafo
        if opcao == 0:
            _grafo = []
            for linha in file:
                _grafo.append({
                    'origem': linha.split(';')[0],
                    'destino': linha.split(';')[1],
                    'custo': int(linha.split(';')[2].split("\n")[0])
                })
            file.close()
            return _grafo
        # abre o arquivo de heuristica
        else:
            _heuristica = []
            for linha in file:
                _heuristica.append({
                    'cidade': linha.split(';')[0],
                    'custo': int(linha.split(';')[1].split("\n")[0])
                })
            file.close()
            return _heuristica

def imprimiFronteira(aberto ,lst_itens):
    print("\nFRONTEIRA:")
    for item in lst_itens:
        print(f"{item['cidade']} {item['custo']} + {item['heuristica']} = {item['custo'] + item['heuristica']}")
    print(f"\nNO ABERTO: {aberto['cidade']} ({aberto['custo'] + aberto['heuristica']})")
    print("-------------------------------")

def imprimiTotal(_total):
    print("\nTOTAL")
    print(f"O melhor caminho de {origem} até {destino} é de {_total}Km")

def imprimiCaminho():
    for city in caminho:
        if city != destino:
            print(f"{city} -> ", end="")
        else:
            print(f"{city}")
    print("-------------------------------\n")

# adiciona as cidades no alcance do No
def abreNo(no_origem):
    _nos_abertos = []
    # cria o primeiro no
    if no_origem is None:
        # vasculha a heuristica
        for no_heuristica in heuristica:
            if no_heuristica["cidade"] == origem:
                # cria o no 
                _nos_abertos.append({
                    'cidade': origem,
                    'custo': 0,
                    'heuristica': no_heuristica["custo"]
                })
                break
    else:
        # vasculha o grafo
        for no in grafo:
            # o nó de origem pode estar como destino ou origem no grafo
            if no['origem'] == no_origem['cidade']:
                # vasculha a heuristica 
                for no_heuristica in heuristica:
                    if no_heuristica["cidade"] == no["destino"]:
                        # cria o no 
                        _nos_abertos.append({
                            'cidade': no['destino'],
                            # custo do no mais do caminho anterior
                            'custo': no['custo'] + no_origem['custo'],
                            'heuristica': no_heuristica["custo"]
                        })
                        break
            elif no['destino'] == no_origem['cidade']:
                # vasculha a heuristica
                for no_heuristica in heuristica:
                    if no_heuristica["cidade"] == no["origem"]:
                        # cria o no 
                        _nos_abertos.append({
                            'cidade': no['origem'],
                            'custo': no['custo'] + no_origem['custo'],
                            'heuristica': no_heuristica["custo"]
                        })
                        break
    return _nos_abertos 

def buscaAestrela(no_origem=None, _fronteira=[]):
    _cidade = None
    if no_origem is not None:
        # adiciona a cidade ao caminho
        _cidade = no_origem['cidade']

        imprimiFronteira(no_origem, _fronteira)
    
        # testa se chegou ao destino
        if no_origem['cidade'] == destino:
            imprimiTotal(no_origem['custo'])
            return [destino]
    
        # remove o Nó a ser aberto da fronteira
        _fronteira.remove(no_origem)
    
    # adiciona a fronteira os novos nos
    _fronteira += abreNo(no_origem)

    # indentifica o no de menor custo
    menor = None
    for _no in _fronteira:
        if menor is None or _no["custo"] + _no["heuristica"] < menor["custo"] + menor["heuristica"]:
            menor = _no
    
    # retorna o caminho
    _caminho = buscaAestrela(menor, _fronteira)

    # Apaga cidades que foram abertas mas não pertencem ao caminho
    for no in grafo:
        if (no['origem'] == _cidade and no['destino'] == _caminho[0]) or (no['destino'] == _cidade and no['origem'] == _caminho[0]):
            return [_cidade] + _caminho
    
    return _caminho

# variaveis gerais do problema
origem = "Arad"
destino = "Bucareste"
grafo = leArquivo("Grafo.txt")
heuristica = leArquivo("Heuristica.txt", 1)

# encontra o resultado da busca
caminho = buscaAestrela()
imprimiCaminho()


