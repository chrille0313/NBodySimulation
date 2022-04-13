from Engine.engine import *
from body import Body
import pygame
from numpy import random


class Game(PygameApp):
	"""
	TODO:
		- Make examples
	"""

	def __init__(self, windowSize: tuple):
		super().__init__(windowSize, 60, camera=Camera2D(Vector2(0, 0), Vector2(windowSize), 1))

		maxSpeed = 10
		bodies = 150
		minMass, maxMass = 500, 10000
		# self.bodies = [Body(Vector2(0, 50), 500, Vector2(0, 3)), Body(Vector2(0, -50), 250, Vector2(0, -3))]
		self.bodies = [Body(Vector2(random.randint(-self.windowSize.x/2, self.windowSize.x/2) * 25,
		                            random.randint(-self.windowSize.y/2, self.windowSize.y/2) * 25),
		               random.randint(minMass, maxMass),
		               Vector2((random.rand() * 2 - 1), (random.rand() * 2 - 1)) * maxSpeed)
		               for _ in range(bodies)]

		yBounds = Vector2(self.windowSize.y/2, -self.windowSize.y/2) * 100
		xBounds = Vector2(-self.windowSize.x/2, self.windowSize.x/2) * 100
		self.bounds = [yBounds.x, xBounds.x, yBounds.y, xBounds.y]

	def on_draw(self):
		for body in self.bodies:
			body.draw(self)

	def on_update(self):
		if self.isKeyPressed[pygame.K_ESCAPE]:
			self.quit()

		if self.isKeyPressed[pygame.K_w]:
			self.mainCamera.pos += Vector2(0, 1) * self.mainCamera.moveSpeed / self.mainCamera.zoom
		if self.isKeyPressed[pygame.K_s]:
			self.mainCamera.pos += Vector2(0, -1) * self.mainCamera.moveSpeed / self.mainCamera.zoom
		if self.isKeyPressed[pygame.K_a]:
			self.mainCamera.pos += Vector2(-1, 0) * self.mainCamera.moveSpeed / self.mainCamera.zoom
		if self.isKeyPressed[pygame.K_d]:
			self.mainCamera.pos += Vector2(1, 0) * self.mainCamera.moveSpeed / self.mainCamera.zoom

		if self.isKeyPressed[pygame.K_q]:
			self.mainCamera.zoom *= self.mainCamera.zoomSpeed
		if self.isKeyPressed[pygame.K_e]:
			self.mainCamera.zoom /= self.mainCamera.zoomSpeed

		# GRAVITY
		for i, body1 in enumerate(self.bodies):
			for body2 in self.bodies:
				if body1 != body2:
					body1.apply_force(body1.gravitational_force(body2))

		# COLLISION DETECTION
		for i, body1 in enumerate(self.bodies):
			for body2 in self.bodies[i:]:
				if body1 != body2:
					body1.collide(body2)

			body1.collide(self.bounds)

		# UPDATE BODIES
		for body in self.bodies:
			body.update(1)


game = Game((800, 800))
game.run()
