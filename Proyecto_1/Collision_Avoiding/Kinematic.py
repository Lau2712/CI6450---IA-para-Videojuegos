from Vector import Vector
from SteeringOutput import SteeringOutput
import random
import math

class Kinematic:
    def __init__(self, position: Vector, orientation: float, velocity: Vector, rotation: float):
        self.position = position
        self.orientation = orientation
        self.velocity = velocity
        self.rotation = rotation
    
    def __init__(self, position: Vector, orientation: float, velocity: Vector, rotation: float):
        self.position = position
        self.orientation = orientation
        self.velocity = velocity
        self.rotation = rotation
        self.time_in_corner = 0
        self.escape_cooldown = 0

    def update(self, steering: SteeringOutput, time: float, maxSpeed: float, screen_width: int, screen_height: int):
        self.position += self.velocity * time
        self.orientation += self.rotation * time
        
        # La velocidad y la rotación
        self.velocity += steering.linear * time
        self.rotation += steering.angular * time
        
        # Aplicar el impulso de escape si es necesario
        escape_impulse = self.calculate_escape_impulse(screen_width, screen_height)
        self.velocity += escape_impulse
        
        # Limita la velocidad
        if self.velocity.magnitude() > maxSpeed:
            self.velocity = self.velocity.normalize() * maxSpeed
        
        # Maneja los límites de la pantalla
        self.handle_screen_bounds(screen_width, screen_height)

        # Reducimos el tiempo del escape
        if self.escape_cooldown > 0:
            self.escape_cooldown -= time

    # Función para calcular el impulso de escape en caso que el personaje se encuentre
    # atrapado en alguna esquina
    def calculate_escape_impulse(self, screen_width: int, screen_height: int) -> Vector:
        corner_threshold = 50 
        escape_threshold = 3  
        escape_strength = 200 

        in_corner = (self.position.x < corner_threshold and self.position.z < corner_threshold) or \
                    (self.position.x < corner_threshold and self.position.z > screen_height - corner_threshold) or \
                    (self.position.x > screen_width - corner_threshold and self.position.z < corner_threshold) or \
                    (self.position.x > screen_width - corner_threshold and self.position.z > screen_height - corner_threshold)

        if in_corner:
            self.time_in_corner += 1/60
        else:
            self.time_in_corner = 0

        if self.time_in_corner > escape_threshold and self.escape_cooldown <= 0:
            center = Vector(screen_width / 2, screen_height / 2)
            escape_direction = (center - self.position).normalize()
            
            # Establecemos un ángulo aleatorio para la dirección
            random_angle = random.uniform(-math.pi/4, math.pi/4)
            escape_direction = escape_direction.rotate(random_angle)
            
            # Debemos esperar 5 segundos antes de escapar de nuevo
            self.escape_cooldown = 5
            self.time_in_corner = 0
            return escape_direction * escape_strength
        
        return Vector(0, 0)

    # Función para manejar los rebotes de la pantalla
    def handle_screen_bounds(self, screen_width: int, screen_height: int):
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