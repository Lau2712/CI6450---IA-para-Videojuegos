from SteeringOutput import SteeringOutput
from Align import Align
from Vector import Vector
import math

class LookWhereYoureGoing(Align):
    def __init__(self, character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)

    def getSteering(self) -> SteeringOutput:
        velocity: Vector = self.character.velocity
        
        if velocity.magnitude() == 0:
            return None

        # Calculamos la orientación basada en la velocidad
        self.target.orientation = math.atan2(-velocity.x, velocity.z)

        # Llamamos al método getSteering de la clase padre (Align)
        return super().getSteering()