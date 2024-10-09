from Vector import Vector
class KinematicSteeringOutput:
    def __init__(self, velocity: Vector, rotation: float):
        self.velocity = velocity
        self.rotation = rotation
    