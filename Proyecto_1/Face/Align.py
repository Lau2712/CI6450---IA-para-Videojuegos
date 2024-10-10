from Kinematic import Kinematic
from Vector import Vector
from SteeringOutput import SteeringOutput
import math

class Align:
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float):
        self.character = character
        self.target = target
        self.maxAngularAcceleration = maxAngularAcceleration
        self.maxRotation = maxRotation
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = timeToTarget

    def getSteering(self) -> SteeringOutput:
        result = SteeringOutput(Vector(0, 0), 0)
        
        # Se obtiene la dirección al objetivo
        rotation = self.target.orientation - self.character.orientation
        
        # Mapeamos el resultado
        rotation = self.mapToRange(rotation)
        rotationSize = abs(rotation)
        
        # Se verifica si estamos dentro del radio
        if rotationSize < self.targetRadius:
            return result
        
        # Si estamos fuera del radio, se mueve a máxima rotación
        if rotationSize > self.slowRadius:
            self.targetRotation = self.maxRotation
        else:
            self.targetRotation = self.maxRotation * rotationSize / self.slowRadius
        
        # Obtenemos la rotación final del objetivo
        self.targetRotation *= rotation / rotationSize
        
        # La aceleración intenta alcanzar a la rotación
        result.angular = self.targetRotation - self.character.rotation
        result.angular /= self.timeToTarget
        
        # Se chequea si la aceleración es muy buena
        angularAcceleration = abs(result.angular)
        if angularAcceleration > self.maxAngularAcceleration:
            result.angular /= angularAcceleration
            result.angular *= self.maxAngularAcceleration
        
        result.linear = Vector(0, 0)
        return result
        
    @staticmethod
    # Función encarga de mapear entre 2 valores específicos
    def mapToRange(rotation):
        return ((rotation + math.pi) % (2 * math.pi)) - math.pi
