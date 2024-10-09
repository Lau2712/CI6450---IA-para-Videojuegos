from Vector import Vector
class static:
    def __init__(self, position: Vector, orientation: float):
        self.position = position
        self.orientation = orientation
        self.x = position.x
        self.z = position.z