from Engine.Core.app import App, Vector2
from Engine.colors import Colors
from math import sqrt, log10


class Body:
	def __init__(self, pos: Vector2, mass: float, vel: Vector2 = None, acc: Vector2 = None, color=Colors.WHITE):
		self.pos = pos
		self.vel = vel if vel is not None else Vector2(0, 0)
		self.acc = acc if acc is not None else Vector2(0, 0)
		self.mass = mass
		self.size = sqrt(mass)

		self.color = color

	def apply_force(self, force: Vector2):
		"""
		Apply force to the body.

		:param force: force to apply
		:return: None
		"""

		self.acc += force / self.mass

	def gravitational_force(self, other: 'Body', G=5) -> Vector2:
		"""
		Calculate the gravitational force between two bodies.

		:param other: other body to calculate the force with
		:param G: gravitational constant (default: 10)
		:return: None
		"""

		displacement = other.pos - self.pos
		direction = displacement.normalize()
		force = (self.mass * other.mass) / max(displacement.magnitude_squared(), (self.size + other.size) ** 2)  # avoid division by zero
		return direction * G * force

	def is_colliding(self, other):
		"""
		Check if two bodies are colliding.

		:param other: other body to check collision with
		:return: True if bodies are colliding, else False
		"""

		if isinstance(other, self.__class__):
			return (self.pos - other.pos).magnitude_squared() <= (self.size + other.size) * (self.size + other.size)
		else:
			top, left, bottom, right = other
			return self.pos.y + self.size >= top, self.pos.x - self.size <= left, self.pos.y - self.size <= bottom, self.pos.x + self.size >= right

	def __discrete_collision(self, other):
		"""
		Perform discrete collision between two bodies.

		:param other: other body to collide with
		:return: None
		"""

		if isinstance(other, self.__class__):
			# return if the bodies are moving away from each other
			# if self.vel.dot(other.vel) > 0:
				# return

			# Calculate the new velocities using conservation of momentum and kinetic energy
			normal = (self.pos - other.pos).normalize()
			p = 2 * (self.vel.dot(normal) - other.vel.dot(normal)) / (self.mass + other.mass)
			self.vel -= p * other.mass * normal
			other.vel += p * self.mass * normal

			# Make sure the bodies don't overlap
			self.pos = other.pos + normal * (other.size + self.size)

		else:
			bounds = self.is_colliding(other)
			newVel = Vector2(-1 if bounds[1] or bounds[3] else 1, -1 if bounds[0] or bounds[2] else 1)
			self.vel = self.vel.elementwise() * newVel

	def __continous_collision(self, other):
		"""
		Perform continous collision between two bodies.

		:param other: other body to collide with
		:return: None
		"""

		pass

	def collide(self, other, continuous=False):
		"""
		Perform collision between two bodies.

		:param other: other body to collide with
		:param continuous: if true, perform continous collision, else discrete
		:return: None
		"""

		if self.is_colliding(other):
			if continuous:
				self.__continous_collision(other)
			else:
				self.__discrete_collision(other)

	def update(self, dt: float):
		"""
		Update the bodies dynamics.

		:param dt: time since last update
		:return: None
		"""

		self.vel += self.acc * dt
		self.pos += self.vel * dt

		self.acc = Vector2(0, 0)  # Reset the acceleration as no force is acting on the body (we don't want to upset Newton)

		colorGrade = min(abs(int(255 * log10(self.vel.magnitude_squared() / self.mass / 2))), 255)
		self.color = (255 - colorGrade, colorGrade, 50)

	def draw(self, app: App):
		"""
		Draw the body in given application.

		:param app: app to draw the body in
		:return:
		"""

		app.draw_circle(Vector2(self.pos.x, self.pos.y), self.size, self.color, fromCamera=True)

	def __str__(self):
		return f"Body(pos={self.pos}, vel={self.vel}, acc={self.acc}, mass={self.mass})"

	def __repr__(self):
		return self.__str__()
