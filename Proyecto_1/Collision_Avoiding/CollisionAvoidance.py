from Kinematic import Kinematic
from SteeringOutput import SteeringOutput
from Vector import Vector

class CollisionAvoidance:
    def __init__(self, character: Kinematic, max_acceleration: float, targets: list, radius: float):
        self.character = character
        self.max_acceleration = max_acceleration
        self.targets = targets
        self.radius = radius
    
    def get_steering(self) -> SteeringOutput:
        shortest_time = float('inf')
        first_target = None
        first_relative_pos = Vector(0, 0)
        
        for target in self.targets:
            relative_pos = target.position - self.character.position
            relative_vel = target.velocity - self.character.velocity
            relative_speed_squared = relative_vel.x**2 + relative_vel.z**2
            
            if relative_speed_squared == 0:
                continue

            time_to_collision = -(relative_pos.x * relative_vel.x + relative_pos.z * relative_vel.z) / relative_speed_squared
            
            distance = relative_pos.magnitude()
            
            if distance < self.radius * 2 and time_to_collision > 0 and time_to_collision < shortest_time:
                shortest_time = time_to_collision
                first_target = target
                first_relative_pos = relative_pos

        if not first_target:
            return None

        # Si hay una colisión inminente, calculamos la dirección de evasión
        avoidance = first_relative_pos.normalize() * -1 
        
        result = SteeringOutput(Vector(0, 0), 0)
        result.linear = avoidance * self.max_acceleration
        result.angular = 0
        return result