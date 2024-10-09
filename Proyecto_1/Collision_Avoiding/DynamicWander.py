from SteeringOutput import SteeringOutput
from Vector import Vector
import random
import math
from FaceBehavior import FaceBehavior

class Wander(FaceBehavior):
    def __init__(self, character, target, max_angular_acceleration, max_rotation, 
                target_radius, slow_radius, time_to_target, wander_offset, 
                wander_radius, wander_rate, max_acceleration):
        super().__init__(character, target, max_angular_acceleration, max_rotation, 
                        target_radius, slow_radius, time_to_target)
        self.character = character
        self.target = target
        self.max_angular_acceleration = max_angular_acceleration
        self.max_rotation = max_rotation
        self.target_radius = target_radius
        self.slow_radius = slow_radius
        self.time_to_target = time_to_target
        self.wander_offset = wander_offset
        self.wander_radius = wander_radius
        self.wander_rate = wander_rate
        self.wander_orientation = random.uniform(0, 2 * math.pi)
        self.max_acceleration = max_acceleration
    
    # Función encargada de generar un número aleatorio
    def randomBinomial(self):
        return random.random() - random.random()
    
    # Función encargada de convertir un angulo a un vector
    def vectorFromAngle(self, angle):
        return Vector(math.cos(angle), math.sin(angle))
    
    # Función encarga de obtener el steering
    def getSteering(self) -> SteeringOutput:
        
        # Actualizamos la orientación del wander
        self.wander_orientation += self.randomBinomial() * self.wander_rate
        
        target_orientation = self.wander_orientation + self.character.orientation
        
        # Calculamos el centro del círculo del wander
        orientation_vector = self.vectorFromAngle(self.character.orientation)
        offset_vector = Vector(orientation_vector.x * self.wander_offset, 
                               orientation_vector.z * self.wander_offset)
        target_position = self.character.position + offset_vector

        # Calculamos el punto del objetivo que se encuentra en el círculo
        displacement = self.vectorFromAngle(target_orientation)
        displacement = Vector(displacement.x * self.wander_radius, 
                              displacement.z * self.wander_radius)
        target_position += displacement
        
        # Implementamos Face para determinar la posición del objetivo
        self.target.position = target_position
        steering = super().getSteering()
        
        # Si steering es None, creamos un nuevo SteeringOutput
        if steering is None:
            steering = SteeringOutput(Vector(0, 0), 0)

        # Obtenemos la aceleración lineal
        acceleration_vector = self.vectorFromAngle(self.character.orientation)
        steering.linear = Vector(acceleration_vector.x * self.max_acceleration,
                                 acceleration_vector.z * self.max_acceleration)

        return steering