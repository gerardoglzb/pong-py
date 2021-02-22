import pygame
from network import Network
from random import uniform
from gameState import GameState


pygame.init()
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
network = None
max_fps = 30
game = None

play_button_size = (240, 120)
play_button_left = screen_size[0] / 2 - play_button_size[0] / 2
play_button_top = screen_size[1] / 2 - play_button_size[1] / 2

running = True
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 75)
waiting_sign = font.render('Waiting...', True, (0, 0, 0))
play_sign = font.render("Play!", True, (0, 0, 0))

game_on = False

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN and not game_on:
			mouse_pos = pygame.mouse.get_pos()
			if mouse_pos[0] >= play_button_left and mouse_pos[0] <= play_button_left + play_button_size[0] and mouse_pos[1] >= play_button_top and mouse_pos[1] <= play_button_top + play_button_size[1]:
				network = Network()
				game_on = True

	screen.fill((255, 255, 255))

	if not game_on:
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(play_button_left, play_button_top, play_button_size[0], play_button_size[1]), 10)
		screen.blit(play_sign, (screen_size[0] / 2 - play_sign.get_width() / 2, screen_size[1] / 2 - play_sign.get_height() / 2))
	else:
		keys = pygame.key.get_pressed()
		right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
		left = keys[pygame.K_a] or keys[pygame.K_LEFT]
		game = network.move_paddle(right - left)
		if game.get_game_state() == GameState.WAITING:
			screen.blit(waiting_sign, (screen_size[0] / 2 - waiting_sign.get_width() / 2, screen_size[1] / 2 - waiting_sign.get_height() / 2))
		elif game.get_game_state() == GameState.ONGOING:
			paddle1 = game.paddles[0]
			paddle2 = game.paddles[1]
			ball = game.ball
			pygame.draw.line(screen, (0, 0, 255), (paddle1.get_x_pos_1(), paddle1.get_y_pos()), (paddle1.get_x_pos_2(), paddle1.get_y_pos()), paddle1.get_width())
			pygame.draw.line(screen, (0, 0, 255), (paddle2.get_x_pos_1(), paddle2.get_y_pos()), (paddle2.get_x_pos_2(), paddle2.get_y_pos()), paddle2.get_width())
			pygame.draw.circle(screen, (255, 0, 0), (ball.get_x_pos(), ball.get_y_pos()), ball.get_radius())

	pygame.display.flip()
	clock.tick(max_fps)

pygame.quit()
