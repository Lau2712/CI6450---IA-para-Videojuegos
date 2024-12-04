from Vector import Vector
import math

class Path:
    def __init__(self, center: Vector, radius: float):
        self.center = center
        self.radius = radius

    def getParam(self, position: Vector, lastParam: float) -> float:
        # Calcular el ángulo entre el centro y la posición dada
        to_position = position - self.center
        angle = math.atan2(to_position.z, to_position.x)
        
        # Asegurar que el ángulo esté en el rango [0, 2π]
        if angle < 0:
            angle += 2 * math.pi
        
        return angle

    def getPosition(self, param: float) -> Vector:
        # Calcular la posición en el círculo para el parámetro dado
        x = self.center.x + self.radius * math.cos(param)
        z = self.center.z + self.radius * math.sin(param)
        return Vector(x, z)