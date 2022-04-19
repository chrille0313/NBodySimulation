from Engine.engine import *

from body import Body
from quadtree import QuadTree

import pygame  # Only for keycodes!
from numpy import random


class Game(PygameApp):
	def __init__(self, windowSize: tuple):
		super().__init__(windowSize, 60, camera=Camera2D(Vector2(0, 0), Vector2(windowSize), 1))

		scale = 1
		self.bounds = Rect(-self.windowSize.x / 2 * scale, self.windowSize.y / 2 * scale, self.windowSize.x * scale, self.windowSize.y * scale)

		bodies = 300
		maxSpeed = 40
		minMass, maxMass = 10, 1000

		self.bodies = []

		for _ in range(bodies):
			pos = Vector2(random.randint(self.bounds.x, (self.bounds.x + self.bounds.width)),
			              random.randint((self.bounds.y - self.bounds.height), self.bounds.y))

			mass = random.randint(minMass, maxMass)

			vel = Vector2(random.randint(-maxSpeed, maxSpeed), random.randint(-maxSpeed, maxSpeed))

			self.bodies.append(Body(pos, mass, vel))

		self.debug = True  # Comment to disable debug mode

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

		# UPDATE BODIES
		for body in self.bodies:
			body.update(1)


game = Game((800, 800))
game.run()
