from Engine.Core.app import App, Vector2
from Engine.colors import Colors


class Body:
	def __init__(self, pos: Vector2, mass: float, vel: Vector2 = None, acc: Vector2 = None, color=Colors.WHITE):
		self.pos = pos
		self.vel = vel if vel is not None else Vector2(0, 0)
		self.acc = acc if acc is not None else Vector2(0, 0)
		self.mass = mass

		self.color = color

	def apply_force(self, force: Vector2):
		"""
		Apply force to the body.

		:param force: force to apply
		:return: None
		"""

		self.acc += force / self.mass

	def gravitational_force(self, other: 'Body'):
		"""
		Calculate the gravitational force between two bodies.

		:param other: other body to calculate the force with
		:return: None
		"""

		return (self.mass * other.mass) / (other.pos - self.pos).magnitude_squared()

	def update(self, dt: float):
		"""
		Update the bodies dynamics.

		:param dt: time since last update
		:return: None
		"""

		self.vel += self.acc * dt
		self.pos += self.vel * dt

	def draw(self, app: App):
		"""
		Draw the body in given application.

		:param app: app to draw the body in
		:return:
		"""

		app.draw_circle(self.pos, self.mass, self.color)

	def __str__(self):
		return f"Body(pos={self.pos}, vel={self.vel}, acc={self.acc}, mass={self.mass})"

	def __repr__(self):
		return self.__str__()
