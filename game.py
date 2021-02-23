from ball import Ball
from paddle import Paddle
from gameState import GameState

class Game():
	def __init__(self, screen_size, paddle_vertical_margin, paddle_length, paddle_width, paddle_speed, ball_radius, ball_speed, ball_velocity):
		self.p1 = False
		self.p2 = False
		self.game_state = GameState.OFF
		paddle1 = Paddle(paddle_vertical_margin, screen_size[0] / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed)
		paddle2 = Paddle(screen_size[1] - paddle_vertical_margin, screen_size[0] / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed)
		self.paddles = [paddle1, paddle2]
		self.ball = Ball(screen_size[0] / 2, screen_size[1] / 2, ball_radius, ball_speed, ball_velocity)

	def set_p1(self, player):
		self.p1 = player

	def set_p2(self, player):
		self.p2 = player

	def get_p1(self):
		return self.p1

	def get_p2(self):
		return self.p2

	def set_game_state(self, state):
		self.game_state = state

	def get_game_state(self):
		return self.game_state

	def get_paddles(self):
		return self.paddles

	def get_ball(self):
		return self.ball
