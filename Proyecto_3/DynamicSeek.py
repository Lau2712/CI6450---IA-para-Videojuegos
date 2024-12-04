from Vector import Vector
from Kinematic import Kinematic
from SteeringOutput import SteeringOutput

class DynamicSeek:
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, max_distance: float, screen_width: int, screen_height: int):
        self.character = character
        self.target = target
        self.max_acceleration = max_acceleration
        self.max_distance = max_distance
        self.screen_width = screen_width
        self.screen_height = screen_height

    def getSteering(self) -> SteeringOutput:
        result = SteeringOutput(Vector(0, 0), 0)
        
        # Se obtiene la dirección del objetivo
        direction = self.target.position - self.character.position
        distance = direction.magnitude()
        
        # Normaliza y escala por la aceleración máxima y la fuerza
        if direction.magnitude() > 0:
            result.linear = direction.normalize() * self.max_acceleration
        else:
            result.linear = Vector(0, 0)

        
        # Añade una pequeña fuerza hacia el centro de la pantalla si estamos cerca de los bordes
        # buffer = 50
        # center_force = Vector(0, 0)
        # if self.character.position.x < buffer:
        #     center_force.x += self.max_acceleration * 0.5
        # elif self.character.position.x > self.screen_width - buffer:
        #     center_force.x -= self.max_acceleration * 0.5
        # if self.character.position.z < buffer:
        #     center_force.z += self.max_acceleration * 0.5
        # elif self.character.position.z > self.screen_height - buffer:
        #     center_force.z -= self.max_acceleration * 0.5
            
        # result.linear += center_force
        result.angular = 0
        
        return result