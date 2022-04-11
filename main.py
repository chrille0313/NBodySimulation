from Engine.Core.core import *
from body import Body


class Game(PygameApp):
	def __init__(self, windowSize: tuple):
		super().__init__(windowSize)

		self.bodies = [Body(self.windowCenter, 10)]

	def on_draw(self):
		for body in self.bodies:
			body.draw(self)

	def on_update(self):
		for body in self.bodies:
			body.apply_force(Vector2(0, 0.1))
			body.update(1)


game = Game((800, 800))
game.run()
