#Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Collision Avoidance
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from DynamicWander import Wander
from CollisionAvoidance import CollisionAvoidance
from SteeringOutput import SteeringOutput
import math
import random

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
WIDTH, HEIGHT = 700, 600
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))

# Nombre de la ventana
pygame.display.set_caption('Get Out of Collisions')

# EDICIÓN DE LA PANTALLA
BLANCO = (255,255,255)

# Definimos el color de fondo
PANTALLA.fill(BLANCO)

# FONDO
fondo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Fondo/28021.jpg").convert()
PANTALLA.blit(fondo, (0, 0))

# PERSONAJE
quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat.png")
quieto_izq = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat - Izq.png")
mouse_quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Raton/MouseSpritesheet1.png")

# Control de FPS
reloj = pygame.time.Clock()

# Creamos instancias para los gatos
# Definir un buffer que nos ayudará a evitar que el gato se acerque mucho a los bordes
CAT_BUFFER = 80

cats = []
wander_behaviors = []
collision_avoidance_behaviors = []

# Inicializamos
mouse = Kinematic(Vector(0, 0), math.pi/2, Vector(0, 0), 0)

# Definimos la velocidad máxima
MAX_SPEED = 100
MAX_ACCELERATION = 100

for _ in range(10):
    x = random.randint(CAT_BUFFER, WIDTH - CAT_BUFFER)
    y = random.randint(CAT_BUFFER, HEIGHT - CAT_BUFFER)
    initial_velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 50
    cat = Kinematic(Vector(x, y), random.uniform(0, 2*math.pi), initial_velocity, 0)
    cats.append(cat)

# Crear instancias de DynamicWander y CollisionAvoidance para cada gato
max_angular_acceleration = math.pi/4
max_rotation = math.pi/8
target_radius = 0.1
slow_radius = 15 
time_to_target = 0.1
wander_offset = 30
wander_radius = 25
wander_rate = math.pi/8
max_acceleration = 50

for cat in cats:
    wander = Wander(cat, mouse, max_angular_acceleration, max_rotation, target_radius, slow_radius, time_to_target, wander_offset, wander_radius, wander_rate, max_acceleration)
    wander_behaviors.append(wander)
    
    collision_avoidance = CollisionAvoidance(cat, 50, [c for c in cats if c != cat], 30)
    collision_avoidance_behaviors.append(collision_avoidance)

# Función encargada de actualizar a los gatos en pantalla
def update_cat(cat, steering, delta_time):
    # Aplicar el steering
    cat.velocity += steering.linear * delta_time
    cat.rotation += steering.angular * delta_time
    
    # Limitar la velocidad
    if cat.velocity.magnitude() > MAX_SPEED:
        cat.velocity = cat.velocity.normalize() * MAX_SPEED
    
    # Actualizar la posición
    cat.position += cat.velocity * delta_time
    
    # Comprobar si el gato está cerca de los bordes y hacer que rebote
    if cat.position.x < CAT_BUFFER:
        cat.position.x = CAT_BUFFER
        cat.velocity.x = abs(cat.velocity.x)
    elif cat.position.x > WIDTH - CAT_BUFFER:
        cat.position.x = WIDTH - CAT_BUFFER
        cat.velocity.x = -abs(cat.velocity.x)
    
    if cat.position.z < CAT_BUFFER:
        cat.position.z = CAT_BUFFER
        cat.velocity.z = abs(cat.velocity.z)
    elif cat.position.z > HEIGHT - CAT_BUFFER:
        cat.position.z = HEIGHT - CAT_BUFFER
        cat.velocity.z = -abs(cat.velocity.z)
    
    # Actualizar la orientación del gato basada en su velocidad
    if cat.velocity.magnitude() > 0:
        cat.orientation = math.atan2(-cat.velocity.x, cat.velocity.z)

# Función encargada de recargar la pantalla
def recargaPantalla():
    # Fondo
    PANTALLA.blit(fondo, (0, 0))

    # Dibujar y actualizar cada gato
    for i, cat in enumerate(cats):
        wander_steering = wander_behaviors[i].getSteering()
        avoidance_steering = collision_avoidance_behaviors[i].get_steering()
        
        combined_steering = SteeringOutput(Vector(0, 0), 0)
        
        if wander_steering:
            combined_steering.linear += wander_steering.linear * 0.5
        if avoidance_steering:
            combined_steering.linear += avoidance_steering.linear * 2
        
        # Limitar la aceleración máxima
        if combined_steering.linear.magnitude() > MAX_ACCELERATION:
            combined_steering.linear = combined_steering.linear.normalize() * MAX_ACCELERATION
        
        # Actualizar la posición y orientación del gato
        update_cat(cat, combined_steering, 1/60)

        # Determinar qué sprite del gato usar basado en la velocidad
        current_sprite = quieto_izq if cat.velocity.x < 0 else quieto

        # Dibujar el gato
        PANTALLA.blit(current_sprite, (int(cat.position.x) - current_sprite.get_width() // 2, 
                                       int(cat.position.z) - current_sprite.get_height() // 2))
        
    # Dibujar el ratón
    mouse_rect = mouse_quieto.get_rect()
    mouse_rect.center = (int(mouse.position.x), int(mouse.position.z))
    PANTALLA.blit(mouse_quieto, mouse_rect)

    # Para actualizar la visualización de la pantalla
    pygame.display.update()

# BUCLE DE JUEGO
while True:
    # FPS
    reloj.tick(60) / 1000.0
    
    # Bucle del juego
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO