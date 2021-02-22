class Ball():
	def __init__(self, x_pos, y_pos, radius, speed, direction):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.radius = radius
		self.speed = speed
		self.direction = direction
		self.is_colliding = False
		self.is_crashing = False
		self.velocity = direction.normalize() * speed

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

	def collides_with_paddle_front(self, paddle):
		is_in_range_x = self.x_pos + self.radius > paddle.get_x_pos_1() and self.x_pos - self.radius < paddle.get_x_pos_2()
		is_in_range_y = self.y_pos + self.radius >= paddle.get_y_pos_1() and self.y_pos - self.radius <= paddle.get_y_pos_2()
		return is_in_range_x and is_in_range_y

	def collides_with_paddle_side(self, paddle):
		comes_from_side = self.x_pos > paddle.get_x_pos_2() or self.x_pos < paddle.get_x_pos_1()
		return comes_from_side and self.collides_with_paddle_front(paddle)

	def collides_with_paddle(self, paddle):
		return self.x_pos + self.radius > paddle.get_x_pos_1() and self.x_pos - self.radius < paddle.get_x_pos_2() and abs(self.y_pos - paddle.get_y_pos()) <= self.radius

	def collides_with_paddles(self, paddles):
		return self.collides_with_paddle_front(paddles[0]) or self.collides_with_paddle_front(paddles[1])

	def crashing_with_walls(self, screen_size):
		return self.x_pos >= screen_size[0] or self.x_pos <= 0

	def crashing_with_ceilings(self, screen_size):
		return self.y_pos >= screen_size[1] or self.y_pos <= 0

	def move(self, paddles, screen_size):
		self.x_pos += self.velocity.x
		self.y_pos += self.velocity.y
		if self.is_crashing and not self.crashing_with_walls(screen_size):
			self.is_crashing = False
		elif not self.is_crashing and self.crashing_with_walls(screen_size):
			self.reverse_x()
			self.is_crashing = True
		elif self.is_crashing and not self.crashing_with_ceilings(screen_size):
			self.is_crashing = False
		elif not self.is_crashing and self.crashing_with_ceilings(screen_size):
			self.reverse_y()
			self.is_crashing = True
		if self.is_colliding and not self.collides_with_paddles(paddles):
			self.is_colliding = False
		elif not self.is_colliding and self.collides_with_paddles(paddles):
			self.reverse_y()
			self.is_colliding = True
		# elif self.collides_with_paddle_front(paddles[0]) or self.collides_with_paddle_front(paddles[1]):
			# self.reverse_y()
