#Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Dynamic Wandering
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from DynamicWander import Wander
import math
import random

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption('Look for the Mouse')

# Edición de la pantalla
BLANCO = (255,255,255)

# Fondo
fondo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Fondo/28021.jpg").convert()
PANTALLA.blit(fondo, (0,0))

# PERSONAJES
# Cargamos las imágenes de los personajes
quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat.png")
quieto_izq = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat - Izq.png")

# Cargamos las imágenes del objetivo/jugador
mouse_quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Raton/MouseSpritesheet1.png")

# Control de FPS
reloj = pygame.time.Clock()

# Creamos las instancias para los gatos y el objetivo
# Definimos un buffer que nos servirá para delimitar la posición del gato en pantalla
# y que no se acerque demasiado a los bordes
CAT_BUFFER = 50

cats = []
wander_behaviors = []
for _ in range(5):
    x = random.randint(CAT_BUFFER, Width - CAT_BUFFER)
    z = random.randint(CAT_BUFFER, Height - CAT_BUFFER)
    initial_velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 50
    cat = Kinematic(Vector(x, z), random.uniform(0, 2*math.pi), initial_velocity, 0)
    cats.append(cat)

# Creamos la instancia inicial del objetivo
mouse = Kinematic(Vector(0, 0), math.pi/2, Vector(0, 0), 0)

# Crear instancias de DynamicWander para cada gato
max_angular_acceleration = math.pi/2
max_rotation = math.pi/8
target_radius = 0.1 
slow_radius = math.pi/4 
time_to_target = 0.1
wander_offset = 50
wander_radius = 25
wander_rate = math.pi/8
max_acceleration = 50
        
for cat in cats:
    wander = Wander(cat, mouse, max_angular_acceleration, max_rotation, target_radius, slow_radius, time_to_target, wander_offset, wander_radius, wander_rate, max_acceleration)
    wander_behaviors.append(wander)

# Función encargada de realizar la actualización de cada gato en pantalla
def update_cat(cat, steering, delta_time, max_speed):
    
    # Aplicamos los valores del steering
    cat.velocity += steering.linear * delta_time
    cat.rotation += steering.angular * delta_time
    
    # Limitamos la velocidad
    if cat.velocity.magnitude() > max_speed:
        cat.velocity = cat.velocity.normalize() * max_speed
    
    # Actualizamos la posición del gato
    cat.position += cat.velocity * delta_time
    
    # Para evitar que el gato se quede pegado en los bordes, aplicamos un rebote
    if cat.position.x < CAT_BUFFER:
        cat.position.x = CAT_BUFFER
        cat.velocity.x = abs(cat.velocity.x)
    elif cat.position.x > Width - CAT_BUFFER:
        cat.position.x = Width - CAT_BUFFER
        cat.velocity.x = -abs(cat.velocity.x)
    
    if cat.position.z < CAT_BUFFER:
        cat.position.z = CAT_BUFFER
        cat.velocity.z = abs(cat.velocity.z)
    elif cat.position.z > Height - CAT_BUFFER:
        cat.position.z = Height - CAT_BUFFER
        cat.velocity.z = -abs(cat.velocity.z)
    
    # Actualizamos la orientación del gato
    if cat.velocity.magnitude() > 0:
        cat.orientation = math.atan2(-cat.velocity.x, cat.velocity.z)

# Función encargada de recargar la pantalla
def recargaPantalla():
    # Fondo
    PANTALLA.blit(fondo, (0, 0))

    # Dibujar y actualizar cada gato
    for i, cat in enumerate(cats):
        steering = wander_behaviors[i].getSteering()
        if steering:
            update_cat(cat, steering, 1/60, 200)

        # Determinar qué sprite del gato usar basado en la orientación
        if math.pi/2 < cat.orientation <= 3*math.pi/2:
            current_sprite = quieto_izq
        else:
            current_sprite = quieto

        # Dibujar el gato
        PANTALLA.blit(current_sprite, (int(cat.position.x) - current_sprite.get_width() // 2, 
                                       int(cat.position.z) - current_sprite.get_height() // 2))

    # Dibujar el ratón (objetivo/jugador)
    mouse_image = mouse_quieto
    mouse_rect = mouse_image.get_rect()
    mouse_rect.center = (int(mouse.position.x), int(mouse.position.z))
    PANTALLA.blit(mouse_image, mouse_rect)
    
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
# FIN BUCLE DE JUEGO #