from Vector import Vector
import math

class Path:
    def __init__(self, center: Vector, radius: float):
        self.center = center
        self.radius = radius

    def getParam(self, position: Vector, lastParam: float) -> float:
        to_position = position - self.center
        # Obtenemos el ángulo entre la posición x, z
        angle = math.atan2(to_position.z, to_position.x)
        
        # Aseguramos que el ángulo esté en el rango deseado
        if angle < 0:
            angle += 2 * math.pi
        
        return angle

    def getPosition(self, param: float) -> Vector:
        # Determinamos la posición en el círculo
        x = self.center.x + self.radius * math.cos(param)
        z = self.center.z + self.radius * math.sin(param)
        return Vector(x, z)
