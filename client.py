import pygame
from network import Network
from random import uniform
from gameState import GameState
from color import Color


pygame.init()
screen_size = (640, 360)
screen = pygame.display.set_mode(screen_size)
network = None
max_fps = 30
game = None

play_button_size = (120, 60)
play_button_left = screen_size[0] / 2 - play_button_size[0] / 2
play_button_top = screen_size[1] / 2 - play_button_size[1] / 2

running = True
clock = pygame.time.Clock()

def render_score_signs(scores):
	return [font.render(str(scores[0]), True, Color.BLACK), font.render(str(scores[1]), True, Color.BLACK)]

font = pygame.font.SysFont(None, 35)
waiting_sign = font.render('Waiting...', True, Color.BLACK)
play_sign = font.render("Play!", True, Color.BLACK)
scores = [0, 0]
score_signs = render_score_signs(scores)

game_on = False

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			network.cancel_connection()
			running = False
			break
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
		if game.get_game_state() == GameState.CANCELLED:
			game = network.close_connection()
		if game.get_game_state() == GameState.WAITING:
			screen.blit(waiting_sign, (screen_size[0] / 2 - waiting_sign.get_width() / 2, screen_size[1] / 2 - waiting_sign.get_height() / 2))
		elif game.get_game_state() == GameState.ONGOING:
			paddles = game.get_paddles()
			paddle1 = paddles[0]
			paddle2 = paddles[1]
			ball = game.get_ball()
			pygame.draw.line(screen, (0, 0, 255), (paddle1.get_x_pos_1(), paddle1.get_y_pos()), (paddle1.get_x_pos_2(), paddle1.get_y_pos()), paddle1.get_width())
			pygame.draw.line(screen, (0, 0, 255), (paddle2.get_x_pos_1(), paddle2.get_y_pos()), (paddle2.get_x_pos_2(), paddle2.get_y_pos()), paddle2.get_width())
			pygame.draw.circle(screen, (255, 0, 0), (ball.get_x_pos(), ball.get_y_pos()), ball.get_radius())
			if game.get_scores() != scores:
				scores = game.get_scores()
				score_signs = render_score_signs(scores)
			screen.blit(score_signs[0], (screen_size[0] - score_signs[0].get_width() - 5, 10))
			screen.blit(score_signs[1], (screen_size[0] - score_signs[1].get_width() - 5, screen_size[1] - score_signs[1].get_height() - 10))
		elif game.get_game_state() == GameState.FINISHED:
			game_on = False
			network = None

	pygame.display.flip()
	clock.tick(max_fps)

pygame.quit()
