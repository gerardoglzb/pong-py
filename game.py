import pygame


class Paddle():
	def __init__(self, y_pos, x_pos, length, width, speed):
		self.y_pos = y_pos
		self.x_pos = x_pos
		self.length = length
		self.width = width
		self.speed = speed

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

	def move_right(self):
		self.x_pos += self.speed

	def move_left(self):
		self.x_pos -= self.speed


pygame.init()

screen_size_x = 1280
screen_size_y = 720
paddle_vertical_margin = 75
paddle_length = 150
paddle_width = 25
paddle_speed = 2

screen = pygame.display.set_mode([screen_size_x, screen_size_y])
paddle1 = Paddle(paddle_vertical_margin, screen_size_x / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed)
paddle2 = Paddle(screen_size_y - paddle_vertical_margin, screen_size_x / 2 - paddle_length / 2, paddle_length, paddle_width, paddle_speed)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT]:
		paddle1.move_left()
	if keys[pygame.K_RIGHT]:
		paddle1.move_right()

	screen.fill((255, 255, 255))

	# pygame.draw.circle(screen, (0, 0, 255), (250, 250), 5)
	pygame.draw.line(screen, (0, 0, 255), (paddle1.get_x_pos_1(), paddle1.get_y_pos()), (paddle1.get_x_pos_2(), paddle1.get_y_pos()), paddle1.get_width())
	pygame.draw.line(screen, (0, 0, 255), (paddle2.get_x_pos_1(), paddle2.get_y_pos()), (paddle2.get_x_pos_2(), paddle2.get_y_pos()), paddle2.get_width())

	pygame.display.flip()

pygame.quit()
