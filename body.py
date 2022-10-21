from Engine.Core.app import App
from Engine.Utils.utils import Colors, Vector2, Rect
from math import sqrt

from typing import Union, Tuple


class Body:
	"""
	A class that represents a body in space.

	Attributes:
		mass: The mass of the body.
		position: The position of the body.
		acceleration: The acceleration of the body.
		velocity: The velocity of the body.
		acceleration: The acceleration of the body.
		color: The color of the body.

	Methods:
		update: Updates the body.
		draw: Draws the body.
		apply_force: Applies a force to the body.
		gravitational_force: Calculates the gravitational force between two bodies.
		is_colliding: Checks if the body is colliding with given object.
		collide: Handles the collision between this body and given object.
	"""

	def __init__(self, pos: Vector2, mass: float, vel: Vector2 = None, acc: Vector2 = None, color=Colors.WHITE):
		self.position = pos
		self.velocity = vel if vel is not None else Vector2(0, 0)
		self.acceleration = acc if acc is not None else Vector2(0, 0)
		self.mass = mass
		self.size = sqrt(mass)
		self.heat = 0

		self.color = color

	def apply_force(self, force: Vector2):
		"""
		Apply force to the body.

		:param force: force to apply
		:return: None
		"""

		self.acceleration += force / self.mass  # F = ma

	def gravitational_force(self, other: 'Body', G: float = 5.0) -> Vector2:
		"""
		Calculate the gravitational force between two bodies.

		:param other: other body to calculate the force with
		:param G: gravitational constant (default: 10)
		:return: Vector2 representing the gravitational force
		"""

		displacement = other.position - self.position
		minDisplacement = self.size + other.size  # Minimum distance between bodies is the sum of their radii
		direction = displacement.normalize()

		force = (self.mass * other.mass) / max(displacement.magnitude_squared(), minDisplacement * minDisplacement)  # Don't divide by zero
		return direction * G * force

	def is_colliding(self, other: Union['Body', Rect]) -> Union[bool, Tuple[bool, bool, bool, bool]]:
		"""
		Check if two bodies are colliding.

		:param other: other body to check collision with
		:return: True if colliding, False otherwise
		"""

		if isinstance(other, self.__class__):
			# If the distance between the two bodies is less than the sum of their radii, they are colliding
			totSize = self.size + other.size
			return (self.position - other.position).magnitude_squared() <= totSize * totSize

		elif isinstance(other, Rect):
			left, top, right, bottom = other.x, other.y, other.x + other.width, other.y - other.height
			return self.position.y + self.size >= top, self.position.x - self.size <= left, self.position.y - self.size <= bottom, self.position.x + self.size >= right

		else:
			raise TypeError(f"Unhandled type! Expected Body or Rect, got {type(other)}")

	def __discrete_collision(self, other):
		"""
		Perform discrete collision between two bodies.

		:param other: other body to collide with
		:return: None
		"""

		if isinstance(other, self.__class__):
			# Make sure the bodies don't overlap by moving them apart based on their mass
			displacement = self.position - other.position
			d = displacement.magnitude()
			intersectionDistance = displacement * (self.size + other.size - d) / d  # minimum distance to make sure bodies don't overlap

			inverseMass = 1 / self.mass
			inverseMassOther = 1 / other.mass

			self.position += intersectionDistance * inverseMass / (inverseMass + inverseMassOther)
			other.position -= intersectionDistance * inverseMassOther / (inverseMass + inverseMassOther)

			vDiff = self.velocity - other.velocity
			if vDiff.dot(displacement.normalize()) > 0.0:
				return  # No collision as bodies are moving apart

			# Calculate the new velocities using conservation of momentum and kinetic energy (elastic collisions)
			# https://en.wikipedia.org/wiki/Elastic_collision

			displacement = self.position - other.position  # Update displacement as we have moved the bodies
			impulse = 2 / (self.mass + other.mass) * vDiff.dot(displacement) / displacement.magnitude_squared() * displacement
			self.velocity -= impulse * other.mass
			other.velocity += impulse * self.mass

			# Calculate the heat of the collision using momentum (only for coloring)
			self.heat += 0.01 * other.mass * other.velocity.magnitude() / self.mass / 10
			other.heat += 0.01 * self.mass * self.velocity.magnitude() / other.mass / 10

		elif isinstance(other, Rect):
			bounds = self.is_colliding(other)

			# Invert the velocity if the body is colliding with the edge of the rectangle
			newVel = Vector2(-1 if bounds[1] or bounds[3] else 1, -1 if bounds[0] or bounds[2] else 1)
			self.velocity = self.velocity.elementwise() * newVel

		else:
			raise TypeError(f"Unhandled type! Expected Body or Rect, got {type(other)}")

	def __continous_collision(self, other: Union['Body', Rect]):
		"""
		Perform continous collision between two bodies.

		:param other: other body to collide with
		:return: None
		"""

		pass

	def collide(self, other: Union['Body', Rect], continuous: bool = False):
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
		self.heat *= 0.99 * dt  # Reduce the heat of the body

		colorGrade = min(self.heat, 1)  # Clamp to 1
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
