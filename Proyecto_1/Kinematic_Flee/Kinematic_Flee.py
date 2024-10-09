# Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Kinematic Flee
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Static import static
from KinematicFlee import KinematicFlee

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption('Run from the Mouse')

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

# Variables de dirección
izquierda = False
derecha = False

# Pasos
cuentaPasos = 0

# MOVIMIENTO DEL PERSONAJE #
# Crear instancias para el gato y el objetivo
cat = static(Vector(pos_inicial_x, pos_inicial_y), 0)
mouse = static(Vector(350, 300), 0)

# Creamos la instancia de KinematicArrive
max_speed = 5
max_distance = 200
kinematic_seek = KinematicFlee(cat, mouse, max_speed, max_distance, Width, Height)

# Función para actualizar la pantalla de juego
def recargaPantalla():
    #Variables globales
    global cuentaPasos
    
    # Fondo
    PANTALLA.blit(fondo, (0, 0))

    # Contador de pasos
    if cuentaPasos + 1 >= 13:
        cuentaPasos = 0
        
    # Obtenemos el Steering
    steering = kinematic_seek.getSteering()
    
    # Actualizar la posición del gato
    cat.position += steering.velocity

    # Mantener al gato dentro de los límites de la pantalla
    cat.position.x = max(0, min(cat.position.x, Width - 40))
    cat.position.z = max(0, min(cat.position.z, Height - 40))
    
    # Se dibuja al gato en su nueva posición
    if steering.velocity.x < 0:
        PANTALLA.blit(saltaIzquierda[cuentaPasos // 1], (int(cat.position.x), int(cat.position.z)))
    elif steering.velocity.x > 0:
        PANTALLA.blit(saltaDerecha[cuentaPasos // 1], (int(cat.position.x), int(cat.position.z)))
    else:
        PANTALLA.blit(quieto, (int(cat.position.x), int(cat.position.z)))
    
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

