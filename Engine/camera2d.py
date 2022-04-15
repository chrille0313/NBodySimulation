from pygame import Vector2


class Camera2D:
	def __init__(self, position: Vector2, imageSize: Vector2, zoom=1, moveSpeed=5, zoomSpeed=1.1):
		self.position = position
		self.imageSize = imageSize
		self.zoom = zoom
		self.moveSpeed = moveSpeed
		self.zoomSpeed = zoomSpeed
