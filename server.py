import socket
import sys
import os
from _thread import *
from gameState import GameState
from game import Game
import pickle

server = "127.0.0.1"
port = 5555
encoding_format = 'utf-8'
header = 64
ball_speed = 3
screen_size = (640, 360)
paddle_vertical_margin = 75
paddle_length = 75
paddle_width = 12
paddle_speed = 10
ball_radius = 5
current_game = Game(screen_size, paddle_vertical_margin, paddle_length, paddle_width, paddle_speed, ball_radius, ball_speed)

player_here = [False, False]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for players...")


def game_thread(conn, p):
    print(f"Player {p} connected!")
    conn.send(str.encode(str(p)))
    finished = False

    while True:
        try:
            data_length = conn.recv(header).decode(encoding_format)
            if data_length:
                data_length = int(data_length)
                data = conn.recv(data_length).decode(encoding_format)
                data = data.split()
                if data[0] == "move":
                    current_game.get_paddles()[int(data[1])-1].shift_x_pos(int(data[2]))
                    ball_state = current_game.get_ball().move(current_game.get_paddles(), screen_size)
                    if ball_state > 0:
                        current_game.increase_score(ball_state-1)
                        current_game.reset_layout()
                elif data[0] == "state":
                    conn.send(str.encode(f"{current_game.get_game_state().value}"))
                elif data[0] == "cancel":
                    break
                if data[0] == "move" or data[0] == "close":
                    if data[0] == "close":
                        current_game.set_game_state(GameState.FINISHED)
                    message = pickle.dumps(current_game)
                    msg_length = len(message)
                    send_length = str(msg_length).encode(encoding_format)
                    send_length += b' ' * (header - len(send_length))
                    conn.send(send_length)
                    conn.send(message)
                    if data[0] == "close":
                        finished = True
                        break
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, e)
            break

    print(f"Player {p} disconnected!")
    player_here[p-1] = False
    if not finished:
        current_game.set_game_state(GameState.CANCELLED)
    conn.close()

while True:
    conn, addr = s.accept()
    p = None
    if player_here[0]:
        p = 2
        player_here[1] = True
        current_game.set_game_state(GameState.ONGOING)
        current_game.set_p2(True)
    else:
        current_game = Game(screen_size, paddle_vertical_margin, paddle_length, paddle_width, paddle_speed, ball_radius, ball_speed)
        p = 1
        player_here[0] = True
        current_game.set_game_state(GameState.WAITING)
        current_game.set_p1(True)
    if p:
        start_new_thread(game_thread, (conn, p))
