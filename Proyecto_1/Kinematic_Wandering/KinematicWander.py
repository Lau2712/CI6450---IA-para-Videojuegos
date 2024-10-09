from Static import static
from KinematicSteeringOutput import KinematicSteeringOutput
from Vector import Vector
import random
import math

class KinematicWander:
    
    def __init__(self, character: static, maxSpeed: float, maxRotation: float):
        self.character = character
        self.maxSpeed = maxSpeed
        self.maxRotation = maxRotation

    def randomBinomial(self):
        return random.random() - random.random()
    
    def asVector(self, orientation):
        return Vector(math.cos(orientation), math.sin(orientation))
    
    def getSteering(self) -> KinematicSteeringOutput:
        result = KinematicSteeringOutput(Vector(0, 0), 0)
        
        # Se obtiene la velocidad de la orientación del vector
        orientationVector = self.asVector(self.character.orientation)
        result.velocity = orientationVector * self.maxSpeed
        
        # Se cambia la orientación
        result.rotation = self.randomBinomial() * self.maxRotation
        
        return result