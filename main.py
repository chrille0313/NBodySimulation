from Engine.Core.core import *
from body import Body


class Game(PygameApp):
	def __init__(self, windowSize: tuple):
		super().__init__(windowSize, 0)

		self.bodies = [Body(self.windowCenter, 10)]

	def on_draw(self):
		for body in self.bodies:
			body.draw(self)

	def on_update(self):
		for body in self.bodies:
			body.apply_force(Vector2(0, 9.82))
			body.update(self.deltaTime)


game = Game((800, 800))
game.run()
