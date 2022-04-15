from Engine.engine import *
from body import Body
from quadtree import QuadTree

import pygame
from pygame import Rect
from numpy import random


class Game(PygameApp):
	"""
	TODO:
		- Make examples
	"""

	def __init__(self, windowSize: tuple):
		super().__init__(windowSize, 60, camera=Camera2D(Vector2(0, 0), Vector2(windowSize), 1))

		scale = 10
		boundScale = 100
		self.bounds = Rect(-self.windowSize.x / 2 * boundScale, self.windowSize.y / 2 * boundScale, self.windowSize.x * boundScale, self.windowSize.y * boundScale)

		bodies = 100
		maxSpeed = 10
		minMass, maxMass = 100, 5000
		# self.bodies = [Body(Vector2(1, 250), 500, Vector2(0, -3)), Body(Vector2(2, -250), 250, Vector2(0, 3))]
		self.bodies = [Body(Vector2(random.randint(self.bounds.x / scale, (self.bounds.x + self.bounds.width) / scale),
		                            random.randint((self.bounds.y - self.bounds.height) / scale, self.bounds.y / scale)),
		               random.randint(minMass, maxMass),
		               Vector2((random.rand() * 2 - 1), (random.rand() * 2 - 1)) * maxSpeed)
		               for _ in range(bodies)]

	def camera_control(self):
		if self.isKeyPressed[pygame.K_w]:
			self.mainCamera.position += Vector2(0, 1) * self.mainCamera.moveSpeed / self.mainCamera.zoom
		if self.isKeyPressed[pygame.K_s]:
			self.mainCamera.position += Vector2(0, -1) * self.mainCamera.moveSpeed / self.mainCamera.zoom
		if self.isKeyPressed[pygame.K_a]:
			self.mainCamera.position += Vector2(-1, 0) * self.mainCamera.moveSpeed / self.mainCamera.zoom
		if self.isKeyPressed[pygame.K_d]:
			self.mainCamera.position += Vector2(1, 0) * self.mainCamera.moveSpeed / self.mainCamera.zoom

		if self.isKeyPressed[pygame.K_q]:
			self.mainCamera.zoom *= self.mainCamera.zoomSpeed
		if self.isKeyPressed[pygame.K_e]:
			self.mainCamera.zoom /= self.mainCamera.zoomSpeed

	def on_draw(self):
		for body in self.bodies:
			body.draw(self)

		# self.quadTree.draw(self)

	def on_update(self):
		if self.isKeyPressed[pygame.K_ESCAPE]:
			self.quit()

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
			body.apply_force(self.quadTree.gravity(body, 0.5))

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
