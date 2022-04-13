from pygame import Vector2


class Camera2D:
	def __init__(self, pos: Vector2, imageSize: Vector2, zoom=1, moveSpeed=5, zoomSpeed=1.1):
		self.pos = pos
		self.imageSize = imageSize
		self.zoom = zoom
		self.moveSpeed = moveSpeed
		self.zoomSpeed = zoomSpeed
