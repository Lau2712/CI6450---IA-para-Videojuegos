from Vector import Vector
from Kinematic import Kinematic
from SteeringOutput import SteeringOutput

class DynamicFlee:
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
        direction = self.character.position - self.target.position
        distance = direction.magnitude()
        
        # Si la distancia es menor que la máxima, aplicamos flee
        if distance < self.max_distance:
            strength = min(1.0, 1.0 - (distance / self.max_distance))

            if direction.magnitude() > 0:
                result.linear = direction.normalize() * self.max_acceleration * strength
            else:
                result.linear = Vector(0, 0)
        else:
            result.linear = Vector(0, 0)
            return result
        
        # Aplicamos un buffer que nos ayude a acercar al centro de la pantalla al personaje
        # en caso tal que se esté acercando mucho a los bordes.
        buffer = 50
        center_force = Vector(0, 0)
        if self.character.position.x < buffer:
            center_force.x += self.max_acceleration * 0.5
        elif self.character.position.x > self.screen_width - buffer:
            center_force.x -= self.max_acceleration * 0.5
        if self.character.position.z < buffer:
            center_force.z += self.max_acceleration * 0.5
        elif self.character.position.z > self.screen_height - buffer:
            center_force.z -= self.max_acceleration * 0.5
            
        result.linear += center_force
        result.angular = 0
        
        return result
    
    
