import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = self.connect()

    def get_player_id(self):
        return self.player_id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as error:
            print(error)
        return None

    def move_paddle(self, movement):
        try:
            self.client.send(str.encode(f"move {self.player_id} {movement}"))
            return self.client.recv(4096).decode()
        except socket.error as error:
            print(error)
        return None

    def move_ball(self):
        try:
            self.client.send(str.encode("ball"))
            return self.client.recv(4096).decode()
        except socket.error as error:
            print(error)
        return None

    def get_state(self):
        try:
            self.client.send(str.encode(f"state"))
            return int(self.client.recv(4096).decode())
        except socket.error as error:
            print(error)
        return None
