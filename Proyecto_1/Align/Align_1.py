# Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Align
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from Align import Align
import math

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption('Look to the Mouse')

# Edición de la pantalla
BLANCO = (255,255,255)

# Fondo
fondo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Fondo/28021.jpg").convert()
PANTALLA.blit(fondo, (0,0))

# PERSONAJES
# Cargamos las imágenes de los personajes
quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Gato/IdleCat.png")

# Establecemos la posición inicial del personaje
pos_inicial_x = 350
pos_inicial_y = 300

# Cargamos la imagen del objetivo/jugador
mouse_quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Raton/MouseSpritesheet1.png")

# Control de FPS
reloj = pygame.time.Clock()

# Creamos instancias para el gato y el objetivo
cat = Kinematic(Vector(pos_inicial_x, pos_inicial_y), 0, Vector(0, 0), 0)
mouse = Kinematic(Vector(350, 300), math.pi/2, Vector(0, 0), 0)

# Crear instancia de Align
maxAngularAcceleration = math.pi/1000
maxRotation = math.pi/16
targetRadius = 0.01
slowRadius = math.pi/2
timeToTarget = 0.5

align = Align(cat, mouse, maxAngularAcceleration, maxRotation,targetRadius, slowRadius, timeToTarget)

# Función encargada de dibujar la flecha que indica la orientación del gato
def draw_arrow(surface, position, angle, color=(255, 0, 0), size=30):
    # Calculamos la posición de la flecha alrededor del gato
    arrow_distance = 50  # Distancia de la flecha al centro del gato
    arrow_x = position[0] + arrow_distance * math.cos(angle)
    arrow_y = position[1] + arrow_distance * math.sin(angle)
    
    tip = (arrow_x + size * math.cos(angle), arrow_y + size * math.sin(angle))
    left = (arrow_x + size * 0.7 * math.cos(angle + math.pi * 0.8),
            arrow_y + size * 0.7 * math.sin(angle + math.pi * 0.8))
    right = (arrow_x + size * 0.7 * math.cos(angle - math.pi * 0.8),
             arrow_y + size * 0.7 * math.sin(angle - math.pi * 0.8))
    
    pygame.draw.polygon(surface, color, [tip, left, right])

# Funcion para recargar la pantalla del juego
def recargaPantalla():

    # Fondo
    PANTALLA.blit(fondo,(0,0))
    
    # Obtener el Steering
    steering = align.getSteering()
    
    if steering:
        cat.rotation += steering.angular
        cat.orientation += cat.rotation
        cat.orientation = align.mapToRange(cat.orientation)

    # Dibujar el gato
    PANTALLA.blit(quieto, (int(cat.position.x) - quieto.get_width() // 2, 
                                   int(cat.position.z) - quieto.get_height() // 2))

    # Dibujar la flecha
    arrow_position = (int(cat.position.x), int(cat.position.z))
    draw_arrow(PANTALLA, arrow_position, cat.orientation)

    # Dibujar el ratón (objetivo/jugador)
    mouse_image = mouse_quieto
    mouse_rect = mouse_image.get_rect()
    
    # Movemos la imágen para que no quede justo sobre el cursor
    offset_x = 30
    offset_y = 0
    mouse_rect.center = (int(mouse.position.x) + offset_x, int(mouse.position.z) + offset_y)
    
    PANTALLA.blit(mouse_image, mouse_rect)
    
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
    
    # Actualizar la posición del objetivo con el mouse
    current_mouse_pos = pygame.mouse.get_pos()
    mouse.position = Vector(current_mouse_pos[0], current_mouse_pos[1])
    mouse.orientation = math.atan2(mouse.position.z - cat.position.z, mouse.position.x - cat.position.x)

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO #
