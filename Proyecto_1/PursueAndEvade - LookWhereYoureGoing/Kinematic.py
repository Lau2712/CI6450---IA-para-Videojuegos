from SteeringOutput import SteeringOutput
from Vector import Vector

class Kinematic:
    def __init__(self, position: Vector, orientation: float, velocity: Vector, rotation: float):
        self.position = position
        self.orientation = orientation
        self.velocity = velocity
        self.rotation = rotation
    
    # Función para actualizar la posición y la orientación
    def update(self, steering: SteeringOutput, time: float, maxSpeed: float, screen_width: int, screen_height: int):
        self.position += self.velocity * time
        self.orientation += self.rotation * time
        
        # La velocidad y la rotación
        self.velocity += steering.linear * time
        self.rotation += steering.angular * time
        
        # Limita la velocidad
        self.velocity = self.velocity.limit(maxSpeed)
        
        # Maneja los límites de la pantalla
        buffer = 10  # Un pequeño buffer para evitar que el gato se pegue al borde
        if self.position.x < buffer:
            self.position.x = buffer
            self.velocity.x = abs(self.velocity.x)  # Invierte la dirección en x si toca el borde izquierdo
        elif self.position.x > screen_width - buffer:
            self.position.x = screen_width - buffer
            self.velocity.x = -abs(self.velocity.x)  # Invierte la dirección en x si toca el borde derecho
        
        if self.position.z < buffer:
            self.position.z = buffer
            self.velocity.z = abs(self.velocity.z)  # Invierte la dirección en y si toca el borde superior
        elif self.position.z > screen_height - buffer:
            self.position.z = screen_height - buffer
            self.velocity.z = -abs(self.velocity.z)  # Invierte la dirección en y si toca el borde inferior


