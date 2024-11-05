from Static import static
from Vector import Vector
from KinematicSteeringOutput import KinematicSteeringOutput
import math

class KinematicFlee:
    def __init__(self, character: static, target: static, maxSpeed: float, maxDistance: float, screen_width: int, screen_height: int):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.maxDistance = maxDistance
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def getSteering(self) -> KinematicSteeringOutput:
        result = KinematicSteeringOutput(Vector(0, 0), 0)
        
        direction = self.character.position - self.target.position
        distance = direction.magnitude()
        
        if distance > 0 and distance < self.maxDistance:
            result.velocity = direction.normalize() * self.maxSpeed * (1 - distance / self.maxDistance)
        else:
            result.velocity = Vector(0, 0)
        
        # Añadir una fuerza para alejarse de los bordes
        edge_force = self.getEdgeForce()
        result.velocity += edge_force
        
        self.character.orientation = self.newOrientation(self.character.orientation, result.velocity)
        result.rotation = 0
        
        return result
    
    def getEdgeForce(self) -> Vector:
        force = Vector(0, 0)
        edge_distance = 50  # Distancia desde el borde para empezar a aplicar la fuerza

        if self.character.position.x < edge_distance:
            force.x += self.maxSpeed * (1 - self.character.position.x / edge_distance)
        elif self.character.position.x > self.screen_width - edge_distance:
            force.x -= self.maxSpeed * (1 - (self.screen_width - self.character.position.x) / edge_distance)

        if self.character.position.z < edge_distance:
            force.z += self.maxSpeed * (1 - self.character.position.z / edge_distance)
        elif self.character.position.z > self.screen_height - edge_distance:
            force.z -= self.maxSpeed * (1 - (self.screen_height - self.character.position.z) / edge_distance)

        return force
        
    def newOrientation(self, current: float, velocity: Vector) -> float:
        if velocity.magnitude() > 0:
            return math.atan2(velocity.z, velocity.x)
        else:
            return current