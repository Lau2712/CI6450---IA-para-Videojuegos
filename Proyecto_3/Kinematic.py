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
        
        # Implementamos un buffer que nos ayudará a evitar que el personaje se pegue a los bordes de la pantalla
        buffer = 10
        # Si se cumple alguna condición se invierten la posición y la velocidad del personaje
        if self.position.x < buffer:
            self.position.x = buffer
            self.velocity.x = abs(self.velocity.x)
        elif self.position.x > screen_width - buffer:
            self.position.x = screen_width - buffer
            self.velocity.x = -abs(self.velocity.x)
            
        # Mismo procedimiento pero en el sentido vertical
        if self.position.z < buffer:
            self.position.z = buffer
            self.velocity.z = abs(self.velocity.z)
        elif self.position.z > screen_height - buffer:
            self.position.z = screen_height - buffer
            self.velocity.z = -abs(self.velocity.z)
            
