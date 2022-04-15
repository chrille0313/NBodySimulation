from Engine.Core.app import App, Vector2
from Engine.colors import Colors
from math import sqrt, log10


class Body:
	def __init__(self, pos: Vector2, mass: float, vel: Vector2 = None, acc: Vector2 = None, color=Colors.WHITE):
		self.position = pos
		self.velocity = vel if vel is not None else Vector2(0, 0)
		self.acceleration = acc if acc is not None else Vector2(0, 0)
		self.mass = mass
		self.size = sqrt(mass)
		self.heat = 1

		self.color = color

	def apply_force(self, force: Vector2):
		"""
		Apply force to the body.

		:param force: force to apply
		:return: None
		"""

		self.acceleration += force / self.mass

	def gravitational_force(self, other: 'Body', G=5) -> Vector2:
		"""
		Calculate the gravitational force between two bodies.

		:param other: other body to calculate the force with
		:param G: gravitational constant (default: 10)
		:return: None
		"""

		displacement = other.position - self.position
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
			return (self.position - other.position).magnitude_squared() <= (self.size + other.size) * (self.size + other.size)
		else:
			left, top, width, height = other
			right, bottom = left + width, top - height
			return self.position.y + self.size >= top, self.position.x - self.size <= left, self.position.y - self.size <= bottom, self.position.x + self.size >= right

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
			normal = (self.position - other.position).normalize()
			p = 2 * (self.velocity.dot(normal) - other.velocity.dot(normal)) / (self.mass + other.mass)
			self.velocity -= p * other.mass * normal
			other.velocity += p * self.mass * normal

			# Make sure the bodies don't overlap
			self.position = other.position + normal * (other.size + self.size)
			self.heat += 0.1 * other.mass * other.velocity.magnitude() / self.mass / 10
			other.heat += 0.1 * self.mass * self.velocity.magnitude() / other.mass / 10
		else:
			bounds = self.is_colliding(other)
			newVel = Vector2(-1 if bounds[1] or bounds[3] else 1, -1 if bounds[0] or bounds[2] else 1)
			self.velocity = self.velocity.elementwise() * newVel

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

		self.velocity += self.acceleration * dt
		self.position += self.velocity * dt

		self.acceleration = Vector2(0, 0)  # Reset the acceleration as no force is acting on the body (we don't want to upset Newton)
		self.heat *= 0.99  # Reduce the heat of the body

		colorGrade = min(self.heat, 1)
		# colorGradeBlue = min(abs(int(log10(self.vel.magnitude_squared() / self.mass / 2))), 1)
		self.color = (255 * colorGrade, 255 * (1 - colorGrade), 0)

	def draw(self, app: App):
		"""
		Draw the body in given application.

		:param app: app to draw the body in
		:return:
		"""

		app.draw_circle(Vector2(self.position.x, self.position.y), self.size, self.color, fromCamera=True)

	def __str__(self):
		return f"Body(pos={self.position}, vel={self.velocity}, acc={self.acceleration}, mass={self.mass})"

	def __repr__(self):
		return self.__str__()
