from Kinematic import Kinematic
from Vector import Vector
from SteeringOutput import SteeringOutput

class VelocityMatch:
    
    def __init__(self, character: Kinematic, target: Kinematic, maxAcceleration: float, timeToTarget: float):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.timeToTarget = 0.1

    def getSteering(self) -> SteeringOutput:
        result = SteeringOutput(Vector(0, 0), 0)
        
        # La aceleración intenta alcanzar la velocidad del objetivo
        result.linear = self.target.velocity - self.character.velocity
        result.linear /= self.timeToTarget
        
        # Se chequea si la aceleración es muy rápida
        if result.linear.magnitude() > self.maxAcceleration:
            result.linear.normalize()
            result.linear *= self.maxAcceleration
        
        result.angular = 0
        return result