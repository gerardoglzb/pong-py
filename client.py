import pygame
from network import Network
from random import uniform
from GameState import GameState


class Paddle():
	def __init__(self, y_pos, x_pos, length, width, speed, network):
		self.y_pos = y_pos
		self.x_pos = x_pos
		self.length = length
		self.width = width
		self.speed = speed
		self.network = network

	def get_x_pos_1(self):
		return self.x_pos

	def set_x_pos(self, x_pos):
		self.x_pos = x_pos

	def get_x_pos_2(self):
		return self.x_pos + self.length

	def get_y_pos(self):
		return self.y_pos

	def get_width(self):
		return self.width

	def move(self, keys):
		movement = keys[pygame.K_LEFT] * -self.speed + keys[pygame.K_RIGHT] * self.speed
		return self.network.move_paddle(movement)

	def get_state(self):
		s = self.network.get_state()
		return GameState(s)


class Ball():
	def __init__(self, x_pos, y_pos, radius, speed, direction, network):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.radius = radius
		self.speed = speed
		self.direction = direction
		self.velocity = direction.normalize() * speed
		self.network = network

	def get_x_pos(self):
		return int(self.x_pos)

	def get_y_pos(self):
		return int(self.y_pos)

	def get_radius(self):
		return int(self.radius)

	def reverse_x(self):
		self.velocity.x *= -1

	def reverse_y(self):
		self.velocity.y *= -1

	def move(self):
		movement = self.network.move_ball()
		movement = movement.split()
		if movement[0] != "position":
			return
		self.x_pos = int(movement[1])
		self.y_pos = int(movement[2])

	def collides_with_paddle(self, paddle):
		return self.x_pos + self.radius > paddle.get_x_pos_1() and self.x_pos - self.radius < paddle.get_x_pos_2() and abs(self.y_pos - paddle.get_y_pos()) <= self.radius


pygame.init()

screen_size_x = 1280
screen_size_y = 720
paddle_vertical_margin = 75
paddle_length = 150
paddle_width = 25
paddle_speed = 2
ball_radius = 10
ball_speed = 4
ball_velocity = pygame.Vector2(uniform(-1, 1), uniform(-1, 1))
max_fps = 60

network = Network()
screen = pygame.display.set_mode([screen_size_x, screen_size_y])
paddle1 = Paddle(paddle_vertical_margin, screen_size_x / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed, network)
paddle2 = Paddle(screen_size_y - paddle_vertical_margin, screen_size_x / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed, network)
paddles = [paddle1, paddle2]
ball = Ball(screen_size_x / 2, screen_size_y / 2, ball_radius, ball_speed, ball_velocity, network)
game_state = GameState.WAITING

running = True
clock = pygame.time.Clock()
while running:
	clock.tick(max_fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if game_state == GameState.WAITING:
		if paddles[int(network.player_id)-1].get_state() == GameState.ONGOING:
			game_state = GameState.ONGOING
	elif game_state == game_state.ONGOING:
		positions_data = paddles[int(network.player_id)-1].move(pygame.key.get_pressed())
		positions_split = positions_data.split()
		if positions_split[0] == "positions":
			paddle1.set_x_pos(int(positions_split[1]))
			paddle2.set_x_pos(int(positions_split[2]))
		else:
			print("Not positions received.")

	screen.fill((255, 255, 255))

	ball.move()
	print("ball", ball.get_x_pos(), ball.get_y_pos())

	pygame.draw.line(screen, (0, 0, 255), (paddle1.get_x_pos_1(), paddle1.get_y_pos()), (paddle1.get_x_pos_2(), paddle1.get_y_pos()), paddle1.get_width())
	pygame.draw.line(screen, (0, 0, 255), (paddle2.get_x_pos_1(), paddle2.get_y_pos()), (paddle2.get_x_pos_2(), paddle2.get_y_pos()), paddle2.get_width())
	pygame.draw.circle(screen, (255, 0, 0), (ball.get_x_pos(), ball.get_y_pos()), ball.get_radius())
	if ball.get_x_pos() >= screen_size_x or ball.get_x_pos() <= 0:
		ball.reverse_x()
	elif ball.get_y_pos() >= screen_size_y or ball.get_y_pos() <= 0:
		ball.reverse_y()
	if ball.collides_with_paddle(paddle1) or ball.collides_with_paddle(paddle2):
		ball.reverse_y()

	pygame.display.flip()

pygame.quit()
