from Static import static
from Vector import Vector
import math
from KinematicSteeringOutput import KinematicSteeringOutput

class KinematicArrive:
    def __init__(self, character: static, target: static, maxSpeed: float, radius: float):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.radius = radius
        self.timeToTarget = 0.25
    
    def getSteering(self) -> KinematicSteeringOutput:
        
        result = KinematicSteeringOutput(Vector(0, 0), 0)
        
        # Se obtiene la dirección al objetivo
        result.velocity = self.target.position - self.character.position
        
        # Se chequea si estamos dentro del radio
        if result.velocity.magnitude() < self.radius:
            return None
        
        # Nos movemos al objetivo intentando lograrlo en el tiempo establecido
        result.velocity = result.velocity * (1 / self.timeToTarget)
        
        # Si es muy rápido, llevarlo a la máxima velocidad
        if result.velocity.magnitude() > self.maxSpeed:
            result.velocity = result.velocity.normalize() * self.maxSpeed
        
        # Establecemos la orientación hacia el objetivo
        self.character.orientation = self.newOrientation(self.character.orientation, result.velocity)
        result.rotation = 0
        
        return result

    # Función encargada de determinar la nueva orientación
    def newOrientation(self, current: float, velocity: Vector) -> float:
        if velocity.magnitude() > 0:
            return math.atan2(velocity.z, velocity.x)
        else:
            return current
