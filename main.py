from Engine.engine import *

from body import Body
from quadtree import QuadTree

import pygame  # Only for keycodes!
from numpy import random


class Game(PygameApp):
	def __init__(self, windowSize: tuple):
		super().__init__(windowSize, 60, camera=Camera2D(Vector2(0, 0), Vector2(windowSize), 1))

		scale = 10
		boundScale = 100
		self.bounds = Rect(-self.windowSize.x / 2 * boundScale, self.windowSize.y / 2 * boundScale, self.windowSize.x * boundScale, self.windowSize.y * boundScale)

		# Generate random bodies
		bodies = 300
		maxSpeed = 40
		minMass, maxMass = 10, 1000

		self.bodies = []  # Large center body

		for _ in range(bodies):
			pos = Vector2(random.randint(self.bounds.x / scale, (self.bounds.x + self.bounds.width) / scale),
			              random.randint((self.bounds.y - self.bounds.height) / scale, self.bounds.y) / scale)

			mass = random.randint(minMass, maxMass)

			self.bodies.append(Body(pos, mass))

		# Give bodies initial velocity to spin around center
		for body in self.bodies:
			toCenter = -body.position.normalize()
			body.velocity = Vector2(toCenter.y, -toCenter.x) * maxSpeed

		self.bodies.append(Body(Vector2(0, 0), 1000000, Vector2(0, 0)))  # Large center body

	def draw_debug(self):
		self.quadTree.draw(self)

	def camera_control(self):
		if self.isKeyPressed[pygame.K_w]:
			self.mainCamera.move(Vector2(0, 1))
		if self.isKeyPressed[pygame.K_s]:
			self.mainCamera.move(Vector2(0, -1))
		if self.isKeyPressed[pygame.K_a]:
			self.mainCamera.move(Vector2(-1, 0))
		if self.isKeyPressed[pygame.K_d]:
			self.mainCamera.move(Vector2(1, 0))

		if self.isKeyPressed[pygame.K_q]:
			self.mainCamera.zoom_in()
		if self.isKeyPressed[pygame.K_e]:
			self.mainCamera.zoom_out()

	def on_draw(self):
		for body in self.bodies:
			body.draw(self)

		if self.debug:
			self.draw_debug()

	def on_update(self):
		if self.isKeyPressed[pygame.K_ESCAPE]:
			self.quit()

		if self.isKeyPressed[pygame.K_SPACE]:
			self.debug = True
		else:
			self.debug = False

		self.camera_control()

		self.quadTree = QuadTree(self.bounds)

		for body in self.bodies:
			self.quadTree.insert(body)

		# GRAVITY
		for body in self.bodies:
			"""
			# NAIVE GRAVITY
			for body2 in self.bodies:
				if body != body2:
					body.apply_force(body.gravitational_force(body2))
			"""

			# QUADTREE GRAVITY
			self.quadTree.gravity(body, 1, 5)

		# COLLISION DETECTION
		for i, body in enumerate(self.bodies):
			"""
			# NAIVE COLLISION DETECTION
			for body2 in self.bodies[i:]:
				if body != body2:
					body.collide(body2)
			"""

			# QUADTREE COLLISION DETECTION
			self.quadTree.collide(body)

			body.collide(self.bounds)

		# UPDATE BODIES
		for body in self.bodies:
			body.update(1)


game = Game((800, 800))
game.run()
