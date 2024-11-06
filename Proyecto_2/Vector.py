import math

class Vector:
    def __init__(self, x, z):
        self.x = x
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.z / scalar)
    
    def __itruediv__(self, scalar):
        self.x /= scalar
        self.z /= scalar
        return self
    
    def limit(self, max_magnitude):
        mag = self.magnitude()
        if mag > max_magnitude:
            return self.normalize() * max_magnitude
        return Vector(self.x, self.z)

    def magnitude(self):
        return math.sqrt(min(self.x**2 + self.z**2, 1e300))
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector(self.x / mag, self.z / mag)
        else:
            return Vector(0, 0)
        
    def rotate(self, angle):
        x = self.x * math.cos(angle) - self.z * math.sin(angle)
        z = self.x * math.sin(angle) + self.z * math.cos(angle)
        return Vector(x, z)