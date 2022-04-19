from Engine.Core.app import App
from Engine.Utils.utils import Vector2, Rect, Colors

from body import Body


class QuadTree:
	def __init__(self, boundary: Rect):
		self.boundary = Rect(boundary)
		self.divided = False
		self.nw, self.ne, self.sw, self.se = None, None, None, None
		self.children = [None, None, None, None]

		self.body = None
		self.bodiesCenter = Vector2(0, 0)
		self.totalMass = 0

	def contains_point(self, point: Vector2):
		return self.boundary.x <= point.x <= self.boundary.x + self.boundary.width and self.boundary.y >= point.y >= self.boundary.y - self.boundary.height

	def contains_body(self, body: 'Body'):
		return not (body.position.x + body.size <= self.boundary.x or
		            body.position.x - body.size >= self.boundary.x + self.boundary.width or
		            body.position.y - body.size >= self.boundary.y or
		            body.position.y + body.size <= self.boundary.y - self.boundary.height)

	def subdivide(self):
		x, y, w, h = self.boundary
		self.nw = QuadTree(Rect(x, y, w / 2, h / 2))
		self.ne = QuadTree(Rect(x + w / 2, y, w / 2, h / 2))
		self.sw = QuadTree(Rect(x, y - h / 2, w / 2, h / 2))
		self.se = QuadTree(Rect(x + w / 2, y - h / 2, w / 2, h / 2))
		self.children = [self.nw, self.ne, self.sw, self.se]
		self.divided = True

	def insert(self, body):
		# QuadTree does not contain the body
		if not (self.boundary.x <= body.position.x <= self.boundary.x + self.boundary.width and self.boundary.y >= body.position.y >= self.boundary.y - self.boundary.height):
			return False

		if not self.divided:  # leaf node
			if self.body is None:  # Empty leaf node
				self.body = body
			else:  # The leaf node is already occupied
				self.subdivide()

				# Update which quadrant the contained body is in as it now has been subdivided
				for child in self.children:
					child.insert(self.body)
				for child in self.children:
					child.insert(body)

				self.body = None
		else:
			# Find which quadrant the body is in and insert it there
			for child in self.children:
				child.insert(body)

		self.bodiesCenter += body.position * body.mass
		self.totalMass += body.mass

	def collide(self, body: 'Body'):
		if not self.contains_body(body):
			return False
		if not self.divided:
			if self.body is None or self.body == body:
				return False
			else:
				body.collide(self.body)
		else:
			for child in self.children:
				child.collide(body)

	def gravity(self, body: 'Body', theta: float):
		if not self.divided:
			if self.body is None or self.body == body:
				return
			else:
				disp = self.body.position - body.position
				totSize = self.body.size + body.size
				body.acceleration += disp.normalize() * self.body.mass / max(disp.magnitude_squared(), totSize*totSize) * 5
				return

		if self.totalMass == 0:
			return

		pos = self.bodiesCenter / self.totalMass
		totMass = self.totalMass
		displacement = (pos - body.position)
		if self.boundary.width * self.boundary.width / displacement.magnitude_squared() < theta:
			body.acceleration += displacement.normalize() * totMass / displacement.magnitude_squared() * 5
			return

		for child in self.children:
			child.gravity(body, theta)

	def draw(self, app: App):
		app.draw_rect((self.boundary.x, self.boundary.y), self.boundary.width, self.boundary.height, Colors.MAGENTA, 1, fromCamera=True)

		if self.divided:
			for child in self.children:
				child.draw(app)
