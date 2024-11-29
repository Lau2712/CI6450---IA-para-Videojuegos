from Kinematic import Kinematic
from SteeringOutput import SteeringOutput
from Vector import Vector

class DynamicArrive:
    def __init__(self, character: Kinematic, target: Kinematic, maxSpeed: float, maxAcceleration: float, targetRadius: float, slowRadius: float, timeToTarget: float):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.maxAcceleration = maxAcceleration
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = 0.1

    def getSteering(self) -> SteeringOutput:
        result = SteeringOutput(Vector(0, 0), 0)

        # Se obtiene la posición del objetivo
        direction = self.target.position - self.character.position
        distance = direction.magnitude()

        if distance < self.targetRadius:
            return None
        
        if distance > self.slowRadius:
            targetSpeed = self.maxSpeed
        else:
            targetSpeed = self.maxSpeed * (distance / self.slowRadius)
        
        targetVelocity = direction.normalize() * targetSpeed
        
        result.linear = targetVelocity - self.character.velocity
        result.linear = result.linear / (self.timeToTarget * 0.5)
        
        if result.linear.magnitude() > self.maxAcceleration:
            result.linear = result.linear.normalize() * self.maxAcceleration

        result.angular = 0
        return result