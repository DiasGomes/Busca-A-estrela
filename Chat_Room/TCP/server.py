import socket
from _thread import *
import sys
import json

# parametros
server = ""
port = 5555
number_of_connections = 2
HEADER_LENGHT = 2048
data = {}

# parametros por linha de comando [ip, porta e numero de conexoes]
if len(sys.argv) > 1:
    server = sys.argv[1]
    if len(sys.argv) > 2:
        port = sys.argv[2]
        if len(sys.argv) > 3:
            number_of_connections = sys.argv[3]

# cria socket para escutar
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server, port))
except socket.error as e:
    print(str(e))

server_socket.listen(number_of_connections)
print("Waiting for a connection")

# controla o chat entre clientes e o servidor  
def chat(conn, addr):
    global currentId
    id = str(addr[0]) + ":" + str(addr[1])
    # envia o id para o proprio cliente
    conn.send(str.encode(str(id)))
    print(f"Connected to: {id}")

    while True:
        try:
            msg_recv = conn.recv(2048).decode('utf-8')
            print(f"client {id}: {msg_recv}")
            if msg_recv == "quit":
                # remove cliente da conexão
                print(f"Server: Goodbye {id}")
                conn.send(str.encode(json.dumps({'Server': f'Goodbye {id}'})))
                del data[id]
                break
            else:
                data[id] = msg_recv
            # reenvia a msg para todos
            conn.sendall(str.encode(json.dumps(data)))
        except Exception as e:
            print("ERRO: ", e)
            break

    print("Connection Closed")
    conn.close()

# espera novas conexoes de clientes
while True:
    conn, addr = server_socket.accept()
    # nova thread para novo cliente
    start_new_thread(chat, (conn, addr))    
    