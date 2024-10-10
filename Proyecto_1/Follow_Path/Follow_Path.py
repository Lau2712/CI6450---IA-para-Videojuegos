#Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Path Following
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from DynamicSeek import DynamicSeek
from FollowPath import FollowPath
from Path import Path

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
WIDTH, HEIGHT = 700, 600
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))

# Nombre de la ventana
pygame.display.set_caption('Cat Following Path')

# EDICIÓN DE LA PANTALLA
BLANCO = (255,255,255)
ROJO = (255, 0, 0)

# Definimos el color de fondo
PANTALLA.fill(BLANCO)

# FONDO
fondo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Fondo/28021.jpg").convert()
PANTALLA.blit(fondo, (-500,-490))

# PERSONAJE
quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat.png")
quieto_izq = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat - Izq.png")

# Control de FPS
reloj = pygame.time.Clock()

# Definimos la ruta circular
circle_center = Vector(WIDTH/2, HEIGHT/2)
circle_radius = 200
path = Path(circle_center, circle_radius)

# Creamos las instancias para el gato
# Iniciando fuera del círculo
cat_position = Vector(WIDTH/2, HEIGHT/2 + circle_radius + 50) 
cat_velocity = Vector(0, 0)
cat = Kinematic(cat_position, 0, cat_velocity, 0)

# Se crea la instancia de FollowPath
max_acceleration = 500
path_offset = 0.1
predict_time = 0.1
max_speed = 200
follow_path_behavior = FollowPath(cat, path, max_acceleration, path_offset, predict_time, 100, WIDTH, HEIGHT)

def recargaPantalla():
    # Fondo
    PANTALLA.blit(fondo, (0, 0))

    # Dibujamos la ruta circular
    pygame.draw.circle(PANTALLA, ROJO, (int(circle_center.x), int(circle_center.z)), int(circle_radius), 2)

    # Obtener el Steering
    steering = follow_path_behavior.getSteering()

    # Actualizamos la posición y velocidad del gato
    cat.update(steering, 1/60, max_speed, WIDTH, HEIGHT)

    # Dibujar el gato
    if cat.velocity.x < 0:
        PANTALLA.blit(quieto_izq, (int(cat.position.x) - quieto_izq.get_width()//2, int(cat.position.z) - quieto_izq.get_height()//2))
    else:
        PANTALLA.blit(quieto, (int(cat.position.x) - quieto.get_width()//2, int(cat.position.z) - quieto.get_height()//2))

    # Para actualizar la visualización de la pantalla
    pygame.display.update()

# BUCLE DE JUEGO
while True:
    # FPS
    reloj.tick(60)
    
    # Bucle del juego
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO
