from Engine.Utils.utils import Vector2


class Camera2D:
	def __init__(self, position: Vector2, imageSize: Vector2, zoom: float = 1.0, moveSpeed: float = 5, zoomSpeed: float = 1.1):
		self.position = position
		self.imageSize = imageSize
		self.zoom = zoom
		self.moveSpeed = moveSpeed
		self.zoomSpeed = zoomSpeed
