import pygame
from network import Network
from random import uniform
from gameState import GameState


pygame.init()
screen = pygame.display.set_mode((1280, 720))
network = Network()
max_fps = 30
game = None

running = True
clock = pygame.time.Clock()
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((255, 255, 255))

	keys = pygame.key.get_pressed()
	game = network.move_paddle(keys[pygame.K_d] - keys[pygame.K_a])
	if game.get_game_state() == GameState.ONGOING:
		paddle1 = game.paddles[0]
		paddle2 = game.paddles[1]
		ball = game.ball
		pygame.draw.line(screen, (0, 0, 255), (paddle1.get_x_pos_1(), paddle1.get_y_pos()), (paddle1.get_x_pos_2(), paddle1.get_y_pos()), paddle1.get_width())
		pygame.draw.line(screen, (0, 0, 255), (paddle2.get_x_pos_1(), paddle2.get_y_pos()), (paddle2.get_x_pos_2(), paddle2.get_y_pos()), paddle2.get_width())
		pygame.draw.circle(screen, (255, 0, 0), (ball.get_x_pos(), ball.get_y_pos()), ball.get_radius())

	# ball.move()
	# print("ball", ball.get_x_pos(), ball.get_y_pos())

	pygame.display.flip()
	clock.tick(max_fps)

pygame.quit()
