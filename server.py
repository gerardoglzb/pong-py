import socket
import sys
import os
from _thread import *
from gameState import GameState
from random import uniform
from pygame import Vector2
from game import Game
import pickle

server = "127.0.0.1"
port = 5555
encoding_format = 'utf-8'
header = 64
player_positions = {"1": 565, "2": 565}
ball_position_x = 640
ball_position_y = 360
ball_speed = 4
ball_velocity = Vector2(uniform(-1, 1), uniform(-1, 1)).normalize()
screen_size = (1280, 720)
paddle_vertical_margin = 75
paddle_length = 150
paddle_width = 25
paddle_speed = 3
ball_radius = 10
max_fps = 60
current_game = Game(screen_size, paddle_vertical_margin, paddle_length, paddle_width, paddle_speed, ball_radius, ball_speed, ball_velocity)

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
            data_length = conn.recv(header).decode(encoding_format)
            if data_length:
                data_length = int(data_length)
                data = conn.recv(data_length).decode(encoding_format)
                data = data.split()
                if data[0] == "move":
                    current_game.get_paddles()[int(data[1])-1].shift_x_pos(int(data[2]))
                    current_game.get_ball().move(current_game.get_paddles())
                    message = pickle.dumps(current_game)
                    msg_length = len(message)
                    send_length = str(msg_length).encode(encoding_format)
                    send_length += b' ' * (header - len(send_length))
                    conn.send(send_length)
                    conn.send(message)
                    # send length of recv
                elif data[0] == "state":
                    conn.send(str.encode(f"{current_game.get_game_state().value}"))
                else:
                    conn.send(str.encode(""))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, e)
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
        current_game.set_game_state(GameState.ONGOING)
        current_game.set_p2(True)
        print(current_game)
    else:
        p = 1
        p1 = True
        current_game.set_game_state(GameState.WAITING)
        current_game.set_p1(True)
        print(current_game)
    print(f"Player {p} disconnected!")
    start_new_thread(game_thread, (conn, p))
