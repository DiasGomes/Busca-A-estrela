import socket

class client():

    def __init__(self, _ip_host, _port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = _ip_host 
        self.port = _port
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        my_id = self.client.recv(2048).decode()
        print(f"Client {my_id} connected")
        return my_id

    def send_and_recv(self, data: str) -> str:
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
        
    def close(self):
        self.client.close()
        print(f"Connection close!")