import pygame
from network import Network


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
		return self.network.move(movement)


pygame.init()

screen_size_x = 1280
screen_size_y = 720
paddle_vertical_margin = 75
paddle_length = 150
paddle_width = 25
paddle_speed = 2
max_fps = 60

network = Network()
screen = pygame.display.set_mode([screen_size_x, screen_size_y])
paddle1 = Paddle(paddle_vertical_margin, screen_size_x / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed, network)
paddle2 = Paddle(screen_size_y - paddle_vertical_margin, screen_size_x / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed, network)
paddles = [paddle1, paddle2]

running = True
clock = pygame.time.Clock()
while running:
	clock.tick(max_fps)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	positions_data = paddles[int(network.player_id)-1].move(pygame.key.get_pressed())
	positions_split = positions_data.split()
	if positions_split[0] == "positions":
		paddle1.set_x_pos(int(positions_split[1]))
		paddle2.set_x_pos(int(positions_split[2]))
	else:
		print("Not positions received.")

	screen.fill((255, 255, 255))

	pygame.draw.line(screen, (0, 0, 255), (paddle1.get_x_pos_1(), paddle1.get_y_pos()), (paddle1.get_x_pos_2(), paddle1.get_y_pos()), paddle1.get_width())
	pygame.draw.line(screen, (0, 0, 255), (paddle2.get_x_pos_1(), paddle2.get_y_pos()), (paddle2.get_x_pos_2(), paddle2.get_y_pos()), paddle2.get_width())

	pygame.display.flip()

pygame.quit()
