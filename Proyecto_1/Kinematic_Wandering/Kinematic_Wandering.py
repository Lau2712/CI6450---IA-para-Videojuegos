# Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Kinematic Wandering
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Static import static
from KinematicWander import KinematicWander
import math

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption('Catch the Cat')

# Edición de la pantalla
BLANCO = (255,255,255)

# Fondo
fondo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Fondo/28021.jpg").convert()
PANTALLA.blit(fondo, (0,0))

# PERSONAJES
# Cargamos las imágenes de los personajes
quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat.png")

saltaDerecha = [pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat 1.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat2.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat3.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat4.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat5.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat6.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat7.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat8.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat9.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat10.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat11.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat12.png")]

saltaIzquierda = [pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat1 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat2  - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat3  - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat4 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat5 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat6 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat7 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat8 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat9 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat10 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat11 - Izq.png"),
                pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/JumpCat12 - Izq.png")]

pos_inicial_x = 50
pos_inicial_y = 200


# Control de FPS
reloj = pygame.time.Clock()

# Variables de dirección
izquierda = False
derecha = False

# Pasos
cuentaPasos = 0

# MOVIMIENTO DEL PERSONAJE #
# Creamos instancias para el gato
cat_position = Vector(350, 300)
cat_orientation = 0
cat = static(cat_position, cat_orientation)

# Creamos la instancia de KinematicArrive
max_speed = 2
max_rotation = 0.1
wander_behavior = KinematicWander(cat, max_speed, max_rotation)

# Función encargada de aplicar el rebote del personaje
def bounce_at_border(position, velocity, orientation):
    new_velocity = Vector(velocity.x, velocity.z)
    new_orientation = orientation

    # Rebote en los bordes horizontales
    if position.x <= 0 or position.x >= Width:
        new_velocity.x = -new_velocity.x
        new_orientation = math.pi - new_orientation

    # Rebote en los bordes verticales
    if position.z <= 0 or position.z >= Height:
        new_velocity.z = -new_velocity.z
        new_orientation = -new_orientation

    return new_velocity, new_orientation

# Función para recargar la pantalla del juego
def recargaPantalla():
    
    #Variables globales
    global cuentaPasos
    
    # Fondo
    PANTALLA.blit(fondo, (0, 0))
    
    # Contador de pasos
    if cuentaPasos + 1 >= 13:
        cuentaPasos = 0
    
    # Obtenemos el Steering
    steering = wander_behavior.getSteering()
    
    # Actualizar la posición y orientación del gato
    cat.position += steering.velocity
    cat.orientation += steering.rotation

    # Si el gato llega a algún borde de la pantalla, rebota
    new_velocity, new_orientation = bounce_at_border(cat.position, steering.velocity, cat.orientation)
    steering.velocity = new_velocity
    cat.orientation = new_orientation
    
    # Mantener al gato dentro de los límites de la pantalla
    cat.position.x = max(0, min(cat.position.x, Width))
    cat.position.z = max(0, min(cat.position.z, Height))
    
    # Dibujar al gato
    if steering.velocity.x < 0:
        PANTALLA.blit(saltaIzquierda[cuentaPasos // 1], (int(cat.position.x), int(cat.position.z)))
    elif steering.velocity.x > 0:
        PANTALLA.blit(saltaDerecha[cuentaPasos // 1], (int(cat.position.x), int(cat.position.z)))
    else:
        PANTALLA.blit(quieto, (int(cat.position.x), int(cat.position.z)))

    cuentaPasos = (cuentaPasos + 1) % 13

    # Para actualizar la visualización de la pantalla
    pygame.display.update()

# BUCLE DE JUEGO #
# Se debe crear un bucle para mantener la pantalla ejecutándose
while True:
    # FPS
    reloj.tick(18)
    
    # Bucle del juego
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO #

