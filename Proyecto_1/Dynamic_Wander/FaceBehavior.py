from Align import Align
from Kinematic import Kinematic
from SteeringOutput import SteeringOutput
from Vector import Vector
import math

class FaceBehavior(Align):
    def __init__(self, character, target, max_angular_acceleration, max_rotation, target_radius, slow_radius, time_to_target):
        super().__init__(character, target, max_angular_acceleration, max_rotation, target_radius, slow_radius, time_to_target)
        self.target = target
    
    def getSteering(self) -> SteeringOutput:
        # 1. Clacular el objetivo para alinear
        direction = self.target.position - self.character.position
        
        # Se chequea por una dirección cero y no se hacen cambios
        if direction.magnitude() == 0:
            return SteeringOutput(Vector(0, 0), 0)
        
        # 2. Alinear
        self.explicit_target = Kinematic(self.target.position, 0, self.target.velocity, 0)
        self.explicit_target.orientation = math.atan2(-direction.x, direction.z)
        
        return super().getSteering()
        