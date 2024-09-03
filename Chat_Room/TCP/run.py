from TCP.client import client
import sys
import json

# parametros
ip = ""
port = 5555
comando = ""

# parametros por linha de comando [ip, porta]
if len(sys.argv) > 1:
    ip = sys.argv[1]
    if len(sys.argv) > 2:
        port = sys.argv[2]

# cria o cliente
my_client = client(ip, port)

# loop de interação do chat
while comando != "quit": 
    comando = input("me: ")
    # envia msg e recebe resposta
    msg_recebida = my_client.send_and_recv(comando)
    # trsnaforma str para dict
    data = json.loads(msg_recebida)
    for item in data:
        # não mostra a propria msg
        if item != my_client.id:
            print(f"{item}: {data[item]}")  

# encerra conexão    
my_client.close()
    
