from Vector import Vector

class SteeringOutput:
    def __init__(self, linear: Vector, angular: float):
        self.linear = linear
        self.angular = angular