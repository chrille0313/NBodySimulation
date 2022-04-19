from Engine.Utils.utils import Vector2


class Camera2D:
	def __init__(self, position: Vector2, imageSize: Vector2, zoom: float = 1.0, moveSpeed: float = 5, zoomSpeed: float = 1.1):
		self.position = position
		self.imageSize = imageSize
		self.zoom = zoom
		self.moveSpeed = moveSpeed
		self.zoomSpeed = zoomSpeed

	def move(self, direction: Vector2, dt: float = 1.0):
		self.position += direction * self.moveSpeed * dt / self.zoom

	def zoom_in(self, dt: float = 1.0):
		self.zoom *= self.zoomSpeed * dt

	def zoom_out(self, dt: float = 1.0):
		self.zoom /= self.zoomSpeed * dt
