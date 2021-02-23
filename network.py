import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.encoding_format = 'utf-8'
        self.header = 64
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

    def send_string(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as error:
            print(error)
        return None

    def send_pickle(self, data):
        try:
            message = data.encode(self.encoding_format)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.encoding_format)
            send_length += b' ' * (self.header - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            game_length = self.client.recv(self.header).decode(self.encoding_format)
            if game_length:
                game_length = int(game_length)
                game = pickle.loads(self.client.recv(game_length))
                return game
        except socket.error as error:
            print(error)
        return None

    def move_paddle(self, movement):
        return self.send_pickle(f"move {self.player_id} {movement}")

    def close_connection(self):
        return self.send_pickle(f"close {self.player_id}")

    def cancel_connection(self):
        self.send_pickle(f"cancel {self.player_id}")

    def get_state(self):
        try:
            self.client.send(str.encode(f"state"))
            return int(self.client.recv(4096).decode())
        except socket.error as error:
            print(error)
        return None
