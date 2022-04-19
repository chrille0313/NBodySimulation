from Engine.engine import *

from body import Body
from quadtree import QuadTree

import pygame
import random


class Game(PygameApp):
	"""
	TODO:
		- Make examples
	"""

	def __init__(self, windowSize: tuple):
		super().__init__(windowSize, 60, camera=Camera2D(Vector2(0, 0), Vector2(windowSize), 1))

		self.bounds = Rect(-self.windowSize.x / 2, self.windowSize.y / 2, self.windowSize.x, self.windowSize.y)

		self.bodies = [Body(Vector2(0, 250), 1000, Vector2(0, -3)), Body(Vector2(0, -250), 250, Vector2(0, 3))]

		"""
		# Uncomment to generate random bodies
		
		bodies = 250
		maxSpeed = 3
		minMass, maxMass = 10, 100
		
		self.bodies = []

		for _ in range(bodies):
			pos = Vector2(random.randint(self.bounds.x, (self.bounds.x + self.bounds.width)),
			              random.randint((self.bounds.y - self.bounds.height), self.bounds.y))

			mass = random.randint(minMass, maxMass)

			vel = Vector2(random.randint(-maxSpeed, maxSpeed), random.randint(-maxSpeed, maxSpeed))

			self.bodies.append(Body(pos, mass, vel))
		"""

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

	def draw_debug(self):
		self.draw_rect(self.bounds[:2], self.bounds[2], self.bounds[3], (255, 255, 255))

		self.quadTree.draw(self)

	def on_draw(self):
		for body in self.bodies:
			body.draw(self)

		if self.debug:
			self.draw_debug()

	def on_update(self):
		if self.isKeyPressed[pygame.K_ESCAPE]:
			self.quit()

		self.camera_control()

		# Build quadtree for faster calculations
		self.quadTree = QuadTree(self.bounds)

		for body in self.bodies:
			self.quadTree.insert(body)

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
