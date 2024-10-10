# Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Dynamic Arrive
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from DynamicArrive import DynamicArrive

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption('Catch the Mouse')

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

# Establecemos la posición inicial del personaje
pos_inicial_x = 50
pos_inicial_y = 200

# Cargamos las imágenes del objetivo/jugador
mouse_quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto1/Raton/MouseSpritesheet1.png")

# Control de FPS
reloj = pygame.time.Clock()

# Pasos
cuentaPasos = 0

# MOVIMIENTO DEL PERSONAJE #
# Creamos instancias para el gato y el objetivo
cat = Kinematic(Vector(pos_inicial_x, pos_inicial_y), 0, Vector(0, 0), 0)
mouse = Kinematic(Vector(350, 300), 0, Vector(0, 0), 0)

# Crear instancia de DynamicArrive
max_speed = 200
max_acceleration = 100
target_radius = 5
slow_radius = 100
time_to_target = 0.1
dynamic_arrive = DynamicArrive(cat, mouse, max_speed, max_acceleration, target_radius, slow_radius, time_to_target)

def recargaPantalla():
    #Variables globales
    global cuentaPasos, pos_inicial_x, pos_inicial_y
    
    # Fondo
    PANTALLA.blit(fondo, (0, 0))
    
    # Contador de pasos
    if cuentaPasos + 1 >= 13:
        cuentaPasos = 0
    
    # Obtenemos el Steering
    steering = dynamic_arrive.getSteering()
    if steering:
        # Se actualiza la posición del gato
        cat.update(steering, 1/30, max_speed, Width, Height)
        pos_inicial_x, pos_inicial_y = cat.position.x, cat.position.z
    else:
        cat.velocity = Vector(0, 0)
    
    # Se dibuja al gato en su nueva posición
    if cat.velocity.x < -0.1:
        PANTALLA.blit(saltaIzquierda[cuentaPasos // 1], (int(pos_inicial_x), int(pos_inicial_y)))
    elif cat.velocity.x > 0.1:
        PANTALLA.blit(saltaDerecha[cuentaPasos // 1], (int(pos_inicial_x), int(pos_inicial_y)))
    else:
        PANTALLA.blit(quieto, (int(pos_inicial_x), int(pos_inicial_y)))
    
    cuentaPasos = (cuentaPasos + 1) % 13

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
    
    # Actualizar la posición del objetivo con el mouse
    mouse_pos = pygame.mouse.get_pos()
    mouse.position = Vector(mouse_pos[0], mouse_pos[1])

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO #

