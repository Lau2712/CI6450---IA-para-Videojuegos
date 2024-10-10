# Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Face
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from FaceBehavior import FaceBehavior
from Align import Align
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

# Cargamos las imágenes del objetivo/jugador
mouse_quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Raton/MouseSpritesheet1.png")

# Control de FPS
reloj = pygame.time.Clock()

# Creamos instancias para los gatos y el objetivo
cats = []
face_behaviors = []
for _ in range(5):
    x = random.randint(0, 700)
    y = random.randint(0, 600)
    cat = Kinematic(Vector(x, y), random.uniform(0, 2*math.pi), Vector(0, 0), 0)
    cats.append(cat)

mouse = Kinematic(Vector(350, 300), math.pi/2, Vector(0, 0), 0)

# Crear instancias de Face para cada gato
max_angular_acceleration = math.pi/300
max_rotation = math.pi/4
target_radius = 0.1
slow_radius = math.pi
time_to_target = 0.01

for cat in cats:
    face = FaceBehavior(cat, mouse, max_angular_acceleration, max_rotation, target_radius, slow_radius, time_to_target)
    face_behaviors.append(face)

# Función para dibujar la flecha de orientación
def draw_arrow(surface, position, angle, color=(255, 0, 0), size=15):
    # Calculamos la posición de la flecha alrededor del gato
    arrow_distance = 50
    arrow_x = position[0] + arrow_distance * math.cos(angle)
    arrow_y = position[1] + arrow_distance * math.sin(angle)
    
    tip = (arrow_x + size * math.cos(angle), arrow_y + size * math.sin(angle))
    left = (arrow_x + size * 0.7 * math.cos(angle + math.pi * 0.8),
            arrow_y + size * 0.7 * math.sin(angle + math.pi * 0.8))
    right = (arrow_x + size * 0.7 * math.cos(angle - math.pi * 0.8),
             arrow_y + size * 0.7 * math.sin(angle - math.pi * 0.8))
    
    pygame.draw.polygon(surface, color, [tip, left, right])

def recargaPantalla():
    
    # Fondo
    PANTALLA.blit(fondo, (0,0))

    # Dibujar y actualizar cada gato
    for i, cat in enumerate(cats):
        
        steering = face_behaviors[i].getSteering()
        if steering:
            cat.update(steering, 1/60, 100, 700, 600)
            
            # Actualizar la orientación del gato
            cat.orientation = math.atan2(mouse.position.z - cat.position.z, 
                                         mouse.position.x - cat.position.x)
            cat.orientation = Align.mapToRange(cat.orientation)
            
        # Dibujar el gato
        PANTALLA.blit(quieto, (int(cat.position.x) - quieto.get_width() // 2, 
                                       int(cat.position.z) - quieto.get_height() // 2))
        
        # Dibujar la flecha
        arrow_position = (int(cat.position.x), int(cat.position.z))
        draw_arrow(PANTALLA, arrow_position, cat.orientation)

    # Dibujar el ratón (objetivo/jugador)
    mouse_image = mouse_quieto
    mouse_rect = mouse_image.get_rect()
    
    # Movemos la imágen para que no quede justo sobre el cursos
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

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO #
