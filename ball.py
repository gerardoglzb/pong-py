class Ball():
	def __init__(self, x_pos, y_pos, radius, speed, direction):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.radius = radius
		self.speed = speed
		self.direction = direction
		print("whito balls")
		self.velocity = direction.normalize() * speed
		print("blak balls")

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

	def move(self, paddles):
		self.x_pos += self.velocity.x
		self.y_pos += self.velocity.y

	def collides_with_paddle(self, paddle):
		return self.x_pos + self.radius > paddle.get_x_pos_1() and self.x_pos - self.radius < paddle.get_x_pos_2() and abs(self.y_pos - paddle.get_y_pos()) <= self.radius