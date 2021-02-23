class Paddle():
	def __init__(self, y_pos, x_pos, length, width, speed):
		self.y_pos = y_pos
		self.x_pos = x_pos
		self.length = length
		self.width = width
		self.speed = speed

	def get_length(self):
		return self.length

	def get_x_pos_1(self):
		return self.x_pos

	def set_x_pos(self, x_pos):
		self.x_pos = x_pos

	def shift_x_pos(self, amount):
		self.set_x_pos(self.get_x_pos_1() + amount * self.speed)

	def get_x_pos_2(self):
		return self.x_pos + self.length

	def get_y_pos(self):
		return self.y_pos

	def get_y_pos_1(self):
		return self.y_pos - self.width / 2

	def get_y_pos_2(self):
		return self.y_pos + self.width / 2

	def get_width(self):
		return self.width
