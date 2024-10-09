# Proyecto 1. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación del algoritmo Velocity Matching
import pygame, sys
from pygame.locals import *
from Vector import Vector
from Kinematic import Kinematic
from VelocityMatch import VelocityMatch

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption('Run with the Mouse')

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

# Crear instancia de VelocityMatch
max_acceleration = 10
time_to_target = 0.5
velocity_match = VelocityMatch(cat, mouse, max_acceleration, time_to_target)

# Declaramos unas variables para detectar si el mouse está detenido
mouse_stopped = False
mouse_stop_threshold = 1
mouse_stop_time = 0
mouse_stop_duration = 500

def recargaPantalla():
    #Variables globales
    global cuentaPasos, pos_inicial_x, pos_inicial_y
    
    # Fondo
    PANTALLA.blit(fondo, (0, 0))
    
    # Actualizamos la posición y velocidad del gato solo si el mouse no está detenido
    # si el mouse está detenido, reducimos la velocidad
    if not mouse_stopped:
        steering = velocity_match.getSteering()
        if steering:
            cat.velocity += steering.linear * dt
            
            # Ajustamos la velocidad del gato para que iguale a la del ratón
            mouse_speed = mouse.velocity.magnitude()
            max_speed = min(200, max(50, mouse_speed * 5.0)) 
            
            if cat.velocity.magnitude() > max_speed:
                cat.velocity = cat.velocity.normalize() * max_speed
                
            cat.position += cat.velocity * dt
    else:
        deceleration = 5 
        if cat.velocity.magnitude() > 0:
            cat.velocity -= cat.velocity.normalize() * deceleration * dt
            
            # Si la magnitud de la velocidad del gato es menor que 1, lo detenemos
            if cat.velocity.magnitude() < 1: 
                cat.velocity = Vector(0, 0)
        cat.position += cat.velocity * dt
    
    # Mantenemos al gato dentro de los límites de la pantalla
    cat.position.x = max(0, min(cat.position.x, 700))
    cat.position.z = max(0, min(cat.position.z, 600))

    # Para hacer más amigable el juego, determinamos el sprite correcto a usar dependiendo
    # de su orientación
    speed = cat.velocity.magnitude()
    animation_speed = max(1, min(3, int(speed / 20)))
    
    if cat.velocity.x < -0.1:
        current_sprite = saltaIzquierda[cuentaPasos // 3]
    elif cat.velocity.x > 0.1:
        current_sprite = saltaDerecha[cuentaPasos // 3]
    else:
        current_sprite = quieto

    # Dibujamos al gato
    sprite_rect = current_sprite.get_rect()
    sprite_rect.center = (int(cat.position.x), int(cat.position.z))
    PANTALLA.blit(current_sprite, sprite_rect)
    
    cuentaPasos = (cuentaPasos + 1) % (13 * animation_speed)

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

# Declaramos unas variables para determinar la última posición del ratón y el tiempo
last_mouse_pos = pygame.mouse.get_pos()
last_time = pygame.time.get_ticks()

while True:
    # FPS
    dt = reloj.tick(60) / 1000.0 
    
    # Bucle del juego
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Actualizamos la posición y velocidad del objetivo con el mouse
    current_time = pygame.time.get_ticks()
    current_mouse_pos = pygame.mouse.get_pos()
    
    # Calculamos la distancia que se ha movido el mouse
    mouse_movement = Vector(current_mouse_pos[0] - last_mouse_pos[0], 
                            current_mouse_pos[1] - last_mouse_pos[1])
    
    if mouse_movement.magnitude() < mouse_stop_threshold:
        mouse_stop_time += current_time - last_time
        if mouse_stop_time >= mouse_stop_duration:
            mouse_stopped = True
    else:
        mouse_stop_time = 0
        mouse_stopped = False

    # Actualizamos la posición y velocidad del objetivo con el mouse
    mouse.position = Vector(current_mouse_pos[0], current_mouse_pos[1])
    if not mouse_stopped:
        mouse.velocity = mouse_movement * (1000 / (current_time - last_time))
    else:
        mouse.velocity = Vector(0, 0)

    last_mouse_pos = current_mouse_pos
    last_time = current_time

    # Llamada a la función de actualización de la ventana
    recargaPantalla()
# FIN BUCLE DE JUEGO #

