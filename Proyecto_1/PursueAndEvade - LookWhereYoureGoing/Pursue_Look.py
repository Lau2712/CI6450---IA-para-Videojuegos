# Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Pursue and Evade/Look Where You're Going
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from PursueAndEvade import Pursue
from LookWhereYoureGoing import LookWhereYoureGoing
import math
import random

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption('Evade all Cats')

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

# Creamos instancias para los gatos y el objetivo
cats = []
pursue_behaviors = []
evade_behaviors = []
look_behaviors = []

for i in range(3):
    x = random.randint(0, 700)
    y = random.randint(0, 600)
    cat = Kinematic(Vector(x, y), random.uniform(0, 2*math.pi), Vector(0, 0), 0)
    cats.append(cat)

    # Los primeros dos gatos persiguen, el tercero evade
    if i < 2:
        pursue = Pursue(cat, None, 100, 200, 700, 600, 1, False)
        pursue_behaviors.append(pursue)
    else:
        evade = Pursue(cat, None, 100, 200, 700, 600, 1, True)
        evade_behaviors.append(evade)

    look = LookWhereYoureGoing(cat, None, math.pi, math.pi/4, 0.1, math.pi/2, 0.1)
    look_behaviors.append(look)

mouse = Kinematic(Vector(350, 300), math.pi/2, Vector(0, 0), 0)

# Declaramos las variables para detectar cuando el ratón se detenga
last_mouse_pos = pygame.mouse.get_pos()
mouse_stopped_time = 0
MOUSE_STOP_THRESHOLD = 100

def recargaPantalla():
    # Fondo
    PANTALLA.blit(fondo, (0, 0))

    # Dibujar y actualizar cada gato
    for i, cat in enumerate(cats):
        if mouse_stopped_time < MOUSE_STOP_THRESHOLD:
            # Actualizamos el comportamiento de evasión
            if i < 2:
                steering = pursue_behaviors[i].getSteering()
            else:
                steering = evade_behaviors[0].getSteering()

            if steering:
                cat.update(steering, 1/60, 100, 700, 600)

            # Actualizamos la orientación
            look_steering = look_behaviors[i].getSteering()
            if look_steering:
                cat.orientation += look_steering.angular * 1/60

        # Determinar qué sprite del gato usar basado en la orientación
        if math.pi/2 < cat.orientation < 3*math.pi/2:
            current_sprite = quieto_izq
        else:
            current_sprite = quieto

        # Dibujar el gato
        PANTALLA.blit(current_sprite, (int(cat.position.x) - current_sprite.get_width() // 2, 
                                       int(cat.position.z) - current_sprite.get_height() // 2))

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
    if current_mouse_pos == last_mouse_pos:
        mouse_stopped_time += reloj.get_time()
    else:
        mouse_stopped_time = 0
        last_mouse_pos = current_mouse_pos

    mouse.position = Vector(current_mouse_pos[0], current_mouse_pos[1])

    # Actualizar el objetivo para los comportamientos
    for pursue in pursue_behaviors:
        pursue.target = mouse
    for evade in evade_behaviors:
        evade.target = mouse
    for look in look_behaviors:
        look.target = mouse

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO #
