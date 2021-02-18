import socket
from _thread import *
from GameState import GameState

server = "127.0.0.1"
port = 5555
game_state = GameState.OFF
player_positions = {"1": 565, "2": 565}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for players...")


def game_thread(conn, p):
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                continue
            data_split = data.split()
            print("dato", data_split[0] == "state")
            if data_split[0] == "move":
                player_positions[data_split[1]] += int(data_split[2])
                conn.send(str.encode(f"positions {player_positions['1']} {player_positions['2']}"))
            elif data_split[0] == "state":
                print("hoooo")
                print("Sending state ", game_state.value)
                conn.send(str.encode(f"{game_state.value}"))
            else:
                print("Movement error.")
                conn.send(str.encode(""))
        except:
            break

    conn.close()

p1 = False
p2 = False

while True:
    conn, addr = s.accept()
    print("Connection detected.")
    p = None
    if p1:
        p = 2
        p2 = True
        game_state = GameState.ONGOING
    else:
        p = 1
        p1 = True
        game_state = GameState.WAITING
    print(f"Player {p} disconnected!")
    start_new_thread(game_thread, (conn, p))
