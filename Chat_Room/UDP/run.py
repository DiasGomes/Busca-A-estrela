from cliente_udp import client
import sys
import json

# parametros
ip = ""
port = 5555
username = "user_default"
comando = ""

# parametros por linha de comando [ip, porta]
if len(sys.argv) > 1:
    ip = sys.argv[1]
    if len(sys.argv) > 2:
        username = sys.argv[2]
        if len(sys.argv) > 3:
            port = sys.argv[3]

# cria o cliente
my_client = client(username, ip, port)

# loop de interação do chat
while comando != "quit": 
    comando = input(f"{my_client.username}: ")
    # envia msg
    msg_recebida = my_client.send_recv(comando)
    data = json.loads(msg_recebida)
    for _id, item in data.items():
        if _id != my_client.id:
            print(f"{item['user']}> {item['message']}")

# encerra conexão    
my_client.close()
    
