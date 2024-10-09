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

# Establecemos la posición inicial del personaje
pos_inicial_x = 350
pos_inicial_y = 300

# Cargamos la imimagen del objetivo/jugador
mouse_quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Raton/MouseSpritesheet1.png")

# Pasos
cuentaPasos = 0

# Control de FPS
reloj = pygame.time.Clock()

# Creamos instancias para el gato y el objetivo
cat = Kinematic(Vector(pos_inicial_x, pos_inicial_y), 0, Vector(0, 0), 0)
mouse = Kinematic(Vector(350, 300), math.pi/2, Vector(0, 0), 0)

# Crear instancia de Align
maxAngularAcceleration = math.pi
maxRotation = math.pi/2
targetRadius = 0.01
slowRadius = math.pi/2
timeToTarget = 0.1

align = Align(cat, mouse, maxAngularAcceleration, maxRotation,targetRadius, slowRadius, timeToTarget)

# Definimos unas variables para detectar cuando el mouse se detenga y así poder establecer la orientación
last_mouse_pos = pygame.mouse.get_pos()
mouse_stopped_time = 0
MOUSE_STOP_THRESHOLD = 500

# Variable para suavizar la rotación
target_orientation = 0

# Funcion para recargar la pantalla del juego
def recargaPantalla():
    global cuentaPasos, pos_inicial_x, pos_inicial_y

    # Fondo
    PANTALLA.blit(fondo,(0,0))

    # Para que sea más amigable solo calcularemos el steering cuando el mouse esté detenido
    if mouse_stopped_time >= MOUSE_STOP_THRESHOLD:
        
        # Calcular la orientación deseada
        dx = mouse.position.x - cat.position.x
        dy = mouse.position.z - cat.position.z
        desired_orientation = math.atan2(dy, dx)

        # Suavizar la transición de la orientación
        angle_difference = (desired_orientation - cat.orientation + math.pi) % (2 * math.pi) - math.pi
        target_orientation = cat.orientation + angle_difference * 0.1

        # Actualizar la orientación del objetivo
        mouse.orientation = target_orientation
        
        # Obtener el Steering
        steering = align.getSteering()
        
        if steering:
            cat.rotation += steering.angular
            cat.orientation += cat.rotation
            cat.orientation = (cat.orientation + math.pi) % (2 * math.pi) - math.pi

    # Nuevamente, para que el juego sea más amigable, nos aseguramos de que el sprite usado sea
    # el que corresponda con la orientación
    if math.cos(cat.orientation) < -0.1:
        current_sprite = quieto_izq
    elif math.cos(cat.orientation) > 0.1:
        current_sprite = quieto
    else:
        current_sprite = quieto

    # Dibujar el gato
    PANTALLA.blit(current_sprite, (int(cat.position.x) - current_sprite.get_width() // 2, 
                                   int(cat.position.z) - current_sprite.get_height() // 2))

    cuentaPasos = (cuentaPasos + 1) % 13
    
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

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO #