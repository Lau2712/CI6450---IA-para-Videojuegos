# Proyecto 2. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación de los algoritmos World Representation y Toma de Decisiones
import pygame, sys
from TileGraph import TileGraph
from A import pathfind_astar
from KinematicArrive import KinematicArrive
from ManhattanHeuristic import ManhattanHeuristic
from KinematicArriveDecision import KinematicArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision, DisappearAction, PlayerAttackingInRangeDecision
from KinematicFleeDecision import KinematicFleeAction, KinematicFleeDecision, Exp2AttackAction
from BombAction import BombAttackAction, BombFleeAction, BombInteractionDecision
from pygame.locals import *
import math

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 700, 600
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption("Stitch's Adventure")

######################################################### EDICIÓN DE LA PANTALLA ######################################################
BLANCO = (255,255,255)

# Fondo
fondo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Fondo/Fondo Original.png").convert()

# Factor de zoom
ZOOM = 1.50

# Ajustamos la visualización del laberinto con el zoom
scaled_maze = pygame.transform.scale(
    fondo, 
    (int(fondo.get_width() * ZOOM), 
     int(fondo.get_height() * ZOOM))
)

####################################################################################################################

# Inicialización de la ventana
PANTALLA.blit(fondo, (0,0))

# Usaremos la representación Tile Graph para representar el laberinto
tile_size = 32
tile_graph = TileGraph(scaled_maze, tile_size)
maze_mask = pygame.mask.from_surface(scaled_maze)
show_path = False

# Límites del mundo
WORLD_WIDTH = scaled_maze.get_width()
WORLD_HEIGHT = scaled_maze.get_height()

# Posición de la cámara
camera_x = 0
camera_y = 0

# Márgenes para activar el movimiento de la cámara
CAMERA_MARGIN = 200
MOVE_SPEED = 5

################################################# PERSONAJES #########################################################
# Cargamos las imágenes del jugador
quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Quieto.png")
quieto_izq = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Quieto_Izq.png")
quieto_abajo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Quieto_abajo.png")
quieto_arriba = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Quieto_arriba.png")

# Movimiento del jugador
movDerecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Corriendo_{i}.png") for i in range(1, 7)]
movIzquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Corriendo_{i}_Izq.png") for i in range(1, 7)]
movSubiendo = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Subiendo_{i}.png") for i in range(1, 7)]
movBajando = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Bajando_{i}.png") for i in range(1, 7)]
ataqueDerecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Disparar_{i}.png") for i in range(1, 6)]
ataqueIzquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Stitch/Disparar_{i}_Izq.png") for i in range(1, 6)]

# Variable para llevar la cuenta de las imágenes de los movimientos
cuentaPasos = 0

# Dirección inicial del jugador
direccion = 'derecha'
    
# Cargamos las imágenes de los enemigos
experimento1 = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Quieto_1.png")
experimento2 = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Quieto_1.png")

# Movimiento del experimento 1
movExp1Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Corriendo_{i}.png") for i in range(1, 6)]
movExp1Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Corriendo_{i}_Izq.png") for i in range(1, 6)]
ataqueExp1Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Ataque_{i}.png") for i in range(1, 5)]
ataqueExp1Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Ataque_{i}_Izq.png") for i in range(1, 5)]
desapareceExp1Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Desaparecer_{i}.png") for i in range(1, 8)]
desapareceExp1Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 1/Desaparecer_{i}_Izq.png") for i in range(1, 8)]

# Movimiento del experimento 2
movExp2Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 2/Corriendo_{i}.png") for i in range(1, 7)]
movExp2Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 2/Corriendo_{i}_Izq.png") for i in range(1, 7)]
ataqueExp2Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 2/Ataque_{i}.png") for i in range(1, 8)]
ataqueExp2Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Experimento 2//Ataque_{i}_Izq.png") for i in range(1, 8)]

# Velocidad de los experimentos
ENEMY_SPEED = 3

# Direcciones iniciales de los experimentos
enemy_directions = ['derecha', 'derecha']

# Contadores de la animación de los experimentos
enemy_animation_counters = [0, 0]

# Obstáculos
obs = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Obstaculos/Bomba.png")

# Secuencia de explosion
explosion = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Obstaculos/Explosión_{i}.png") for i in range(1, 13)]

# Premios
taza = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Obstaculos/Taza.png")
pastel = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto2/Obstaculos/Pastel.png")

# Variables de escalas para los jugadores/experimentos/bombas
PLAYER_SCALE = 1.5
ENEMY_SCALE = 1.2
BOMB_SCALE = 1.5
GIFTS_SCALE = 1.5

scaled_player = pygame.transform.scale(quieto,(int(quieto.get_width() * PLAYER_SCALE), int(quieto.get_height() * PLAYER_SCALE)))

# Posición del jugador en el mundo
player_x = 0
player_y = 700 

scaled_experimento1 = pygame.transform.scale(experimento1,(int(experimento1.get_width() * ENEMY_SCALE),int(experimento1.get_height() * ENEMY_SCALE)))

scaled_experimento2 = pygame.transform.scale(experimento2,(int(experimento2.get_width() * ENEMY_SCALE),int(experimento2.get_height() * ENEMY_SCALE)))

scaled_bomb = pygame.transform.scale(obs,(int(obs.get_width() * BOMB_SCALE),int(obs.get_height() * BOMB_SCALE)))

scaled_taza = pygame.transform.scale(taza,(int(taza.get_width() * GIFTS_SCALE),int(taza.get_height() * GIFTS_SCALE)))
scaled_pastel = pygame.transform.scale(pastel,(int(pastel.get_width() * GIFTS_SCALE),int(pastel.get_height() * GIFTS_SCALE)))

# Posiciones y características de los experimentos
enemy_positions = [
    {"x": 1000, "y": 680, "sprite": scaled_experimento1, "sprites_right": movExp1Derecha, "sprites_left": movExp1Izquierda, "is_attacking": False, "is_visible": True, "is_disappearing": False},
    {"x": 1300, "y": 200, "sprite": scaled_experimento2, "sprites_right": movExp2Derecha, "sprites_left": movExp2Izquierda, "is_attacking": False, "is_visible": True, "is_disappearing": False}
]

# Posiciones de las bombas
bomb_positions = [{"x": 900, "y": 1200}, {"x": 1650, "y": 600}, {"x": 1075, "y": 450}, {"x": 500, "y": 200},
                  {"x": 1600, "y": 850}, {"x": 1620, "y": 850}, {"x": 1620, "y": 870}, {"x": 1600, "y": 870}]

# Estados de las bombas
bomb_states = [{"exploding": False, "frame": 0} for _ in bomb_positions]

# Posiciones de los regalos
taza_position = [1600, 200]
pastel_position = [1350, 900]

# Variables de los regalos
taza_visible = False
pastel_visible = False
ARRIVAL_RADIUS_GIFT = 10
exp1_pathfinding = False
exp2_pathfinding = False
exp1_path = None
exp2_path = None

# Control de FPS
reloj = pygame.time.Clock()

# Variables de las acciones del experimento 1
DETECTION_RADIUS = 200
ARRIVAL_RADIUS = 100
MAX_SPEED = 4
EXP1_MIN_X = 850
EXP1_MAX_X = 1150

# Variables de las acciones del experimento 2
EXP2_DETECTION_RADIUS = 100
EXP2_FLEE_SPEED = 5
EXP2_MIN_X = 400
EXP2_MAX_X = 1650

# Variables de las acciones del jugador
BOMB_DETECTION_RADIUS = 100
BOMB_EXPLOSION_SPEED = 0.2

# Variables para pathfinding
current_path = None
target_exp = None
current_sprite = quieto
pathfinding_active = False

# Función para verificar si el jugador colisiona con el laberinto
def check_collision(x, y):
    # Obtener el color del píxel en la posición del jugador
    try:
        color = scaled_maze.get_at((int(x), int(y)))
        
        return color[0] < 246 
    except IndexError:
        return True

# Función para obtener el camino entre dos puntos
def get_path(start_x: int, start_y: int, end_x: int, end_y: int):
    start_node = tile_graph.nodes.get((start_x // tile_size, start_y // tile_size))
    end_node = tile_graph.nodes.get((end_x // tile_size, end_y // tile_size))
    
    if start_node and end_node:
        heuristic = ManhattanHeuristic(end_node)
        path = pathfind_astar(tile_graph, start_node, end_node, heuristic)
        return path
    return None

# Función para obtener el camino entre el experimento y el regalo
def get_experiment_path(exp_x, exp_y, target_x, target_y):
    path = get_path(int(exp_x), int(exp_y), int(target_x), int(target_y))
    return path

# Función para determinar si el jugador está en el radio de detección del experimento 1
def test_player_in_range_and_zone_exp1(enemy_pos, player_pos):
    dx = player_pos[0] - enemy_pos[0]
    dy = player_pos[1] - enemy_pos[1]
    distance = math.sqrt(dx*dx + dy*dy)
    
    # Detectamos si el jugador está dentro del radio de detección
    in_range = distance <= DETECTION_RADIUS
    
    # Se expande el área cuando se persigue al jugador
    if in_range:
        in_zone = EXP1_MIN_X - 100 <= enemy_pos[0] <= EXP1_MAX_X + 100
    else:
        in_zone = EXP1_MIN_X <= enemy_pos[0] <= EXP1_MAX_X
    
    return in_range and in_zone

# Función para encontrar el experimento más cercano en base al path finding
def encontrar_experimento_cercano(player_x, player_y, enemy_positions):
    mejor_distancia = float('inf')
    mejor_camino = None
    experimento_objetivo = None

    for enemy in enemy_positions:
        camino = get_path(player_x, player_y, enemy["x"], enemy["y"])
        if camino:
            # Calculamos la longitud del camino
            distancia = len(camino)
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_camino = camino
                experimento_objetivo = enemy

    return mejor_camino, experimento_objetivo

def reset_experiment1():
    enemy_positions[0]["x"] = 1000
    enemy_positions[0]["y"] = 680
    global exp1_pathfinding, pastel_visible
    exp1_pathfinding = False
    pastel_visible = False

def reset_experiment2():
    global exp2_pathfinding, taza_visible
    exp2_pathfinding = False 
    taza_visible = False
    
# Función para dibujar el camino
def draw_path(screen, path, camera_x, camera_y):
    if path:
        # Se dibujan los nodos
        for i in range(len(path)-1):
            start = path[i].from_node
            end = path[i].to_node
            
            start_pos = (start.x * tile_size - camera_x, 
                        start.y * tile_size - camera_y)
            end_pos = (end.x * tile_size - camera_x,
                      end.y * tile_size - camera_y)
            
            pygame.draw.line(screen, (255,0,0), start_pos, end_pos, 2)

# BUCLE DE JUEGO
while True:
    # FPS
    reloj.tick(60)
    
    # Bucle del juego
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    new_x = player_x
    new_y = player_y

    # Velocidad de la animación
    animacion_velocidad = 0.2
    
    if keys[pygame.K_LEFT]:
        new_x -= MOVE_SPEED
        direccion = 'izquierda'
        cuentaPasos += animacion_velocidad
        if cuentaPasos >= len(movIzquierda):
            cuentaPasos = 0
        current_sprite = movIzquierda[int(cuentaPasos)]
        
    elif keys[pygame.K_RIGHT]:
        new_x += MOVE_SPEED
        direccion = 'derecha'
        cuentaPasos += animacion_velocidad
        if cuentaPasos >= len(movDerecha):
            cuentaPasos = 0
        current_sprite = movDerecha[int(cuentaPasos)]
        
    elif keys[pygame.K_UP]:
        new_y -= MOVE_SPEED
        direccion = 'arriba'
        cuentaPasos += animacion_velocidad
        if cuentaPasos >= len(movSubiendo):
            cuentaPasos = 0
        current_sprite = movSubiendo[int(cuentaPasos)]
        
    elif keys[pygame.K_DOWN]:
        new_y += MOVE_SPEED
        direccion = 'abajo'
        cuentaPasos += animacion_velocidad
        if cuentaPasos >= len(movBajando):
            cuentaPasos = 0
        current_sprite = movBajando[int(cuentaPasos)]
        
    elif keys[pygame.K_SPACE]:
        show_path = True
        pathfinding_active = True
        current_path, target_exp = encontrar_experimento_cercano(player_x, player_y, enemy_positions)

        # Si se utilizó path finding
        if current_path:
            next_node = current_path[0].to_node
            target_x = next_node.x * tile_size
            target_y = next_node.y * tile_size
            
            # Se calcula la dirección de movimiento
            dx = target_x - player_x
            dy = target_y - player_y
            dist = ((dx**2 + dy**2)**0.5)
            
            if dist > 0:
                dx = dx/dist * MOVE_SPEED  
                dy = dy/dist * MOVE_SPEED
                
                new_x = player_x + dx
                new_y = player_y + dy
                
                if abs(dx) > abs(dy):
                    direccion = 'derecha' if dx > 0 else 'izquierda'
                    current_sprite = movDerecha[int(cuentaPasos)] if dx > 0 else movIzquierda[int(cuentaPasos)]
                else:
                    direccion = 'arriba' if dy < 0 else 'abajo'
                    current_sprite = movSubiendo[int(cuentaPasos)] if dy < 0 else movBajando[int(cuentaPasos)]
            
                cuentaPasos += animacion_velocidad
                if cuentaPasos >= len(movDerecha):
                    cuentaPasos = 0
                
                if not check_collision(new_x, new_y):
                    player_x = new_x
                    player_y = new_y
            
            # Se dibuja el path
            draw_path(PANTALLA, current_path, camera_x, camera_y)
    
    elif keys[pygame.K_x]:
        cuentaPasos += animacion_velocidad
        if cuentaPasos >= len(ataqueDerecha):
            cuentaPasos = 0
        current_sprite = ataqueDerecha[int(cuentaPasos)] if direccion == 'derecha' else ataqueIzquierda[int(cuentaPasos)]
        scaled_current_sprite = pygame.transform.scale(
            current_sprite,
            (int(current_sprite.get_width() * PLAYER_SCALE),
            int(current_sprite.get_height() * PLAYER_SCALE))
        )
    
    elif keys[pygame.K_c]:
        taza_visible = True
        show_path = True
        exp2_path = get_experiment_path(enemy_positions[1]["x"], enemy_positions[1]["y"], taza_position[0], taza_position[1])
        exp2_pathfinding = True
        
        if exp2_path:
            draw_path(PANTALLA, exp2_path, camera_x, camera_y)
            
            next_node = exp2_path[0].to_node
            target_x = next_node.x * tile_size
            target_y = next_node.y * tile_size
            
            # Se calcula la dirección de movimiento
            dx = target_x - enemy["x"]
            dy = target_y - enemy["y"]
            dist = ((dx**2 + dy**2)**0.5)
            
            if dist > 0:
                dx = dx/dist * ENEMY_SPEED
                enemy_positions[1]["x"] += dx
                
                enemy_animation_counters[1] += 0.2
                if enemy_animation_counters[1] >= len(movExp2Derecha):
                    enemy_animation_counters[1] = 0
                    
                current_frame = int(enemy_animation_counters[1])
                sprites = movExp2Derecha if dx > 0 else movExp2Izquierda
                
                enemy_positions[1]["sprite"] = pygame.transform.scale(
                    sprites[current_frame],
                    (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(sprites[current_frame].get_height() * ENEMY_SCALE))
                )
    
    elif keys[pygame.K_v]:
        pastel_visible = True
        show_path : True
        exp1_path = get_experiment_path(enemy_positions[0]["x"], enemy_positions[0]["y"], pastel_position[0], pastel_position[1])
        exp1_pathfinding = True
        
        if exp1_path:
            draw_path(PANTALLA, exp1_path, camera_x, camera_y)
            next_node = exp1_path[0].to_node
            target_x = next_node.x * tile_size
            target_y = next_node.y * tile_size
            
            # Se calcula la dirección de movimiento
            dx = target_x - enemy_positions[0]["x"]
            dy = target_y - enemy_positions[0]["y"]
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 0:       
                new_x_exp1 = enemy_positions[0]["x"] + dx
                new_y_exp1 = enemy_positions[0]["y"] + dy
                
                if not check_collision(new_x_exp1, new_y_exp1):
                    enemy_positions[0]["x"] = new_x_exp1
                    enemy_positions[0]["y"] = new_y_exp1
                    
                enemy_directions[0] = 'derecha' if dx > 0 else 'izquierda'
                enemy_animation_counters[0] += 0.2
                
                if enemy_animation_counters[0] >= len(movExp1Derecha):
                    enemy_animation_counters[0] = 0
                    
                current_frame = int(enemy_animation_counters[0])
                sprites = movExp1Derecha if dx > 0 else movExp1Izquierda
                
                enemy_positions[0]["sprite"] = pygame.transform.scale(
                    sprites[current_frame],
                    (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(sprites[current_frame].get_height() * ENEMY_SCALE))
                )
        
    else:
        show_path = False
        current_path = None
        cuentaPasos = 0
        if direccion == 'derecha':
            current_sprite = quieto
        elif direccion == 'izquierda':
            current_sprite = quieto_izq
        elif direccion == 'arriba':
            current_sprite = quieto_arriba
        else:
            current_sprite = quieto_abajo

    # Se escala la imagen del sprite actual
    scaled_current_sprite = pygame.transform.scale(current_sprite,(int(current_sprite.get_width() * PLAYER_SCALE),int(current_sprite.get_height() * PLAYER_SCALE)))

    # Verificar colisiones antes de actualizar la posición
    if not check_collision(new_x, new_y):
        player_x = new_x
        player_y = new_y
    
    # Limitar al jugador dentro del mundo
    player_x = max(scaled_player.get_width()//2, min(WORLD_WIDTH - scaled_player.get_width()//2, player_x))
    player_y = max(scaled_player.get_height()//2, min(WORLD_HEIGHT - scaled_player.get_height()//2, player_y))
    
    # Actualizar la cámara
    player_screen_x = player_x - camera_x
    player_screen_y = player_y - camera_y
    
    if player_screen_x > Width - CAMERA_MARGIN:
        camera_x += player_screen_x - (Width - CAMERA_MARGIN)
    elif player_screen_x < CAMERA_MARGIN:
        camera_x += player_screen_x - CAMERA_MARGIN
        
    if player_screen_y > Height - CAMERA_MARGIN:
        camera_y += player_screen_y - (Height - CAMERA_MARGIN)
    elif player_screen_y < CAMERA_MARGIN:
        camera_y += player_screen_y - CAMERA_MARGIN
    
    camera_x = max(0, min(camera_x, WORLD_WIDTH - Width))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - Height))
    
    # Dibujar
    PANTALLA.fill((0, 0, 0))
    PANTALLA.blit(scaled_maze, (-camera_x, -camera_y))
    
    # Dibujamos la representación del mundo
    tile_graph.draw_world_representation(PANTALLA, camera_x, camera_y)
    
    # Actualizamos la posición y animación de los experimientos
    for i, enemy in enumerate(enemy_positions):
        if i == 0:
            if exp1_pathfinding:
                dx = pastel_position[0] - enemy_positions[0]["x"]
                dy = pastel_position[1] - enemy_positions[0]["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < ARRIVAL_RADIUS_GIFT:
                    reset_experiment1()
                else:
                    exp1_path = get_experiment_path(enemy["x"], enemy["y"], pastel_position[0], pastel_position[1])
                    
                    if exp1_path:
                        next_node = exp1_path[0].to_node
                        target_x = next_node.x * tile_size
                        target_y = next_node.y * tile_size
                        
                        dx = target_x - enemy["x"]
                        dy = target_y - enemy["y"]
                        dist = math.sqrt(dx*dx + dy*dy)
                        
                        if dist > 0:
                            
                            new_x_exp1 = enemy["x"] + dx
                            new_y_exp1 = enemy["y"] + dy
                            
                            if not check_collision(new_x_exp1, new_y_exp1):
                                enemy["x"] = new_x_exp1
                                enemy["y"] = new_y_exp1
                            else:
                                enemy["x"] = enemy["x"] + 5
                                enemy["y"] = enemy["y"] + 5
                                
                            enemy_directions[i] = 'derecha' if dx > 0 else 'izquierda'
                            enemy_animation_counters[i] += 0.2
                            
                            if enemy_animation_counters[i] >= len(movExp1Derecha):
                                enemy_animation_counters[i] = 0
                                
                            current_frame = int(enemy_animation_counters[i])
                            sprites = movExp1Derecha if dx > 0 else movExp1Izquierda
                            
                            enemy["sprite"] = pygame.transform.scale(
                                sprites[current_frame],
                                (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                                int(sprites[current_frame].get_height() * ENEMY_SCALE))
                            )
                            
                        draw_path(PANTALLA, exp1_path, camera_x, camera_y)
            else:
                # Si no se está utilizando pathfinding
                if not pathfinding_active:
                    # Definimos las acciones del experimento 1
                    # Kinematic Arrive
                    kinematic_action = KinematicArriveAction(enemy, (player_x, player_y), MAX_SPEED, ARRIVAL_RADIUS)
                    # Patrulla
                    patrol_action = PatrolAction(enemy, enemy_directions[i])
                    # Ataque
                    attack_action = AttackAction(enemy, enemy_directions[i], ataqueExp1Derecha, ataqueExp1Izquierda)
                    # Desaparecer
                    disappear_action = DisappearAction(enemy, enemy_directions[i],desapareceExp1Derecha,desapareceExp1Izquierda)
                    
                    # Se determina la decisión de patrullar o aplicar kinematic
                    chase_decision = InRangeDecision((enemy["x"], enemy["y"]),(player_x, player_y),kinematic_action,patrol_action,test_player_in_range_and_zone_exp1)
                    
                    # Se determina la decision de atacar
                    attack_decision = PlayerReachedDecision((enemy["x"], enemy["y"]),(player_x, player_y),attack_action,chase_decision,ARRIVAL_RADIUS)
                    
                    # Variable para definir si el jugador está atacando
                    player_is_attacking = keys[pygame.K_x]
                    
                    # Se determina la decisión de desaparecer
                    disappear_decision = PlayerAttackingInRangeDecision((enemy["x"], enemy["y"]),(player_x, player_y),player_is_attacking,DETECTION_RADIUS,disappear_action,attack_decision)
                    
                    # Variable acción para determinar que se va a realizar
                    action = disappear_decision.make_decision()
                    
                    # Si se desaparece
                    if action == "disappear":
                        enemy["is_disappearing"] = True
                        enemy["is_attacking"] = False
                        
                        if player_is_attacking:
                            enemy_animation_counters[i] += 0.2
                            disappear_sprites = desapareceExp1Derecha if enemy_directions[i] == 'derecha' else desapareceExp1Izquierda
                        
                            if enemy_animation_counters[i] >= len(disappear_sprites):
                                enemy_animation_counters[i] = len(disappear_sprites) - 1
                                enemy["is_visible"] = False

                            current_frame = int(enemy_animation_counters[i])
                            if current_frame < len(disappear_sprites):
                                enemy["sprite"] = pygame.transform.scale(
                                    disappear_sprites[current_frame],
                                    (int(disappear_sprites[current_frame].get_width() * ENEMY_SCALE),
                                    int(disappear_sprites[current_frame].get_height() * ENEMY_SCALE))
                                )
                        else:
                            enemy["is_disappearing"] = False
                            enemy["is_visible"] = True
                            enemy_animation_counters[i] = 0

                    elif not player_is_attacking:
                        enemy["is_visible"] = True 
                        enemy["is_disappearing"] = False
                        if action == "attack":
                            enemy["is_attacking"] = True
                            enemy_animation_counters[i] += 0.2
                            attack_sprites = ataqueExp1Derecha if enemy_directions[i] == 'derecha' else ataqueExp1Izquierda
                            
                            if enemy_animation_counters[i] >= len(attack_sprites):
                                enemy_animation_counters[i] = 0
                                enemy["is_attacking"] = False
                            
                            current_frame = int(enemy_animation_counters[i])
                            
                            if current_frame >= len(attack_sprites):
                                current_frame = None
                                continue
                                #current_frame = len(attack_sprites) - 1
                                
                            enemy["sprite"] = pygame.transform.scale(
                                attack_sprites[current_frame],
                                (int(attack_sprites[current_frame].get_width() * ENEMY_SCALE),
                                int(attack_sprites[current_frame].get_height() * ENEMY_SCALE))
                            )

                        elif isinstance(action, KinematicArrive):
                            enemy["is_attacking"] = False
                            steering = action.getSteering()
                            if steering:
                                new_x = enemy["x"] + steering.velocity.x
                                enemy["x"] = new_x
                                enemy_directions[i] = 'derecha' if steering.velocity.x > 0 else 'izquierda'
                                
                        elif action == "patrol":
                            enemy["is_attacking"] = False
                            if enemy_directions[i] == 'derecha':
                                new_x = enemy["x"] + ENEMY_SPEED
                            else:
                                new_x = enemy["x"] - ENEMY_SPEED
                            
                            if check_collision(new_x, enemy["y"]):
                                enemy_directions[i] = 'izquierda' if enemy_directions[i] == 'derecha' else 'derecha'
                            else:
                                enemy["x"] = new_x
                
                else:
                    enemy["is_attacking"] = False
                    enemy["is_disappearing"] = False
                    
        # Experimento 2
        else:
            if exp2_pathfinding:
                dx = taza_position[0] - enemy_positions[1]["x"]
                dy = taza_position[1] - enemy_positions[1]["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < ARRIVAL_RADIUS_GIFT:
                    reset_experiment2()
                else:
                    exp2_path = get_experiment_path(enemy["x"], enemy["y"], taza_position[0], taza_position[1])
                    
                    if exp2_path:
                        next_node = exp2_path[0].to_node
                        target_x = next_node.x * tile_size
                        dx = target_x - enemy["x"]
                        
                        if dx > 0:
                            dx = 10
                            new_x = enemy["x"] + dx
                            
                            if EXP2_MIN_X <= new_x <= EXP2_MAX_X:
                                enemy["x"] = new_x
                                
                                current_direction = 'derecha' if dx > 0 else 'izquierda'
                                if enemy_directions[i] != current_direction:
                                    enemy_directions[i] = current_direction
                                    enemy_animation_counters[i] = 0
                                
                                sprites = movExp2Derecha if dx > 0 else movExp2Izquierda
                                
                                enemy_animation_counters[i] = (enemy_animation_counters[i] + 0.2) % len(sprites)
                                current_frame = int(enemy_animation_counters[i])
                                
                                enemy["sprite"] = pygame.transform.scale(
                                    sprites[current_frame],
                                    (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                                    int(sprites[current_frame].get_height() * ENEMY_SCALE))
                                )
                            
                        draw_path(PANTALLA, exp2_path, camera_x, camera_y)
            else:
                if not pathfinding_active:
                    # Definimos las acciones del experimento 2
                    kinematic_flee = KinematicFleeAction(enemy,(player_x, player_y),EXP2_FLEE_SPEED,EXP2_DETECTION_RADIUS,WORLD_WIDTH,WORLD_HEIGHT,EXP2_MIN_X,EXP2_MAX_X)
                    attack_action = Exp2AttackAction(enemy, enemy_directions[i],ataqueExp2Derecha,ataqueExp2Izquierda)
                    patrol_action = PatrolAction(enemy, enemy_directions[i])

                    # Variable para definir si el jugador está atacando
                    player_is_attacking = keys[pygame.K_x]
                    
                    # Árbol de decisión
                    decision_tree = KinematicFleeDecision(enemy,(player_x, player_y),player_is_attacking,EXP2_DETECTION_RADIUS,kinematic_flee,attack_action,patrol_action,EXP2_MIN_X,EXP2_MAX_X)

                    # Determinar acción
                    action = decision_tree.make_decision()

                    if isinstance(action, KinematicFleeAction):
                        enemy["is_attacking"] = False
                        steering = action.getSteering()
                        if steering:
                            new_x = enemy["x"] + steering.velocity.x
                            if EXP2_MIN_X <= new_x <= EXP2_MAX_X:
                                enemy["x"] = new_x
                            enemy_directions[i] = 'derecha' if steering.velocity.x > 0 else 'izquierda'
                            
                    elif action == "attack":
                        enemy["is_attacking"] = True
                        enemy_animation_counters[i] += 0.2
                        attack_sprites = ataqueExp2Derecha if enemy_directions[i] == 'derecha' else ataqueExp2Izquierda
                        
                        if enemy_animation_counters[i] >= len(attack_sprites):
                            enemy_animation_counters[i] = 0
                            enemy["is_attacking"] = False
                        
                        current_frame = int(enemy_animation_counters[i])
                        if current_frame >= len(attack_sprites):
                            current_frame = len(attack_sprites) - 1
                            
                        enemy["sprite"] = pygame.transform.scale(
                            attack_sprites[current_frame],
                            (int(attack_sprites[current_frame].get_width() * ENEMY_SCALE),
                            int(attack_sprites[current_frame].get_height() * ENEMY_SCALE))
                        )
                    elif action == "patrol":
                        enemy["is_attacking"] = False
                        if enemy_directions[i] == 'derecha':
                            new_x = enemy["x"] + ENEMY_SPEED
                            if new_x > EXP2_MAX_X:
                                enemy_directions[i] = 'izquierda'
                        else:
                            new_x = enemy["x"] - ENEMY_SPEED
                            if new_x < EXP2_MIN_X:
                                enemy_directions[i] = 'derecha'
                                
                        enemy["x"] = new_x

                else:
                    enemy["is_attacking"] = False
            
        # Actualizar animación
        if not enemy["is_attacking"] and not enemy["is_disappearing"] :
            if taza_visible and not pastel_visible:
                enemy_animation_counters[0] += 0.2
                if enemy_directions[0] == 'derecha':
                    sprites = enemy_positions[0]["sprites_right"]
                else:
                    sprites = enemy_positions[0]["sprites_left"]
                
                if enemy_animation_counters[0] >= len(sprites):
                    enemy_animation_counters[0] = 0
                    
                current_frame = int(enemy_animation_counters[0])
                enemy_positions[0]["sprite"] = pygame.transform.scale(
                    sprites[current_frame],
                    (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(sprites[current_frame].get_height() * ENEMY_SCALE))
                )
            elif not taza_visible and pastel_visible:
                enemy_animation_counters[1] += 0.2
                if enemy_directions[1] == 'derecha':
                    sprites = enemy_positions[1]["sprites_right"]
                else:
                    sprites = enemy_positions[1]["sprites_left"]
                
                if enemy_animation_counters[1] >= len(sprites):
                    enemy_animation_counters[1] = 0
                    
                current_frame = int(enemy_animation_counters[1])
                enemy_positions[1]["sprite"] = pygame.transform.scale(
                    sprites[current_frame],
                    (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(sprites[current_frame].get_height() * ENEMY_SCALE))
                )
            elif not taza_visible and not pastel_visible:
                enemy_animation_counters[i] += 0.2
                if enemy_directions[i] == 'derecha':
                    sprites = enemy["sprites_right"]
                else:
                    sprites = enemy["sprites_left"]
                
                if enemy_animation_counters[i] >= len(sprites):
                    enemy_animation_counters[i] = 0
                    
                current_frame = int(enemy_animation_counters[i])
                enemy["sprite"] = pygame.transform.scale(
                    sprites[current_frame],
                    (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(sprites[current_frame].get_height() * ENEMY_SCALE))
                )
    
    # Lógica para la decición del jugador y la explosión de las bombas
    bombs_in_range = []
    for i, (bomb, state) in enumerate(zip(bomb_positions, bomb_states)):
        if bomb:
            dx = player_x - bomb["x"]
            dy = player_y - bomb["y"]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= BOMB_DETECTION_RADIUS:
                state["exploding"] = True
                bombs_in_range.append(bomb)

                # Definimos las acciones del jugador
                bomb_attack = BombAttackAction((player_x, player_y), direccion, ataqueDerecha, ataqueIzquierda)
                bomb_flee = BombFleeAction((player_x, player_y), bombs_in_range, EXP2_FLEE_SPEED, BOMB_DETECTION_RADIUS, WORLD_WIDTH, WORLD_HEIGHT)

                # Definimos el árbol de decisión
                bomb_decision = BombInteractionDecision((player_x, player_y), bomb_positions, BOMB_DETECTION_RADIUS, bomb_attack, bomb_flee)

                # Obtenemos la decisión del jugador
                action = bomb_decision.make_decision()
                if action == "attack":
                    cuentaPasos += animacion_velocidad
                    if cuentaPasos >= len(ataqueDerecha):
                        cuentaPasos = 0
                    current_sprite = ataqueDerecha[int(cuentaPasos)] if direccion == 'derecha' else ataqueIzquierda[int(cuentaPasos)]
                    scaled_current_sprite = pygame.transform.scale(
                        current_sprite,
                        (int(current_sprite.get_width() * PLAYER_SCALE),
                        int(current_sprite.get_height() * PLAYER_SCALE))
                    )
                    
                elif isinstance(action, BombFleeAction):
                    steering = action.getSteering()
                    if steering:
                        new_x = player_x + steering.velocity.x
                        new_y = player_y + steering.velocity.z
                        if not check_collision(new_x, new_y):
                            player_x = new_x
                            player_y = new_y
                            
            if state["exploding"]:
                state["frame"] += BOMB_EXPLOSION_SPEED
                if state["frame"] < len(explosion):
                    explosion_sprite = explosion[int(state["frame"])]
                    scaled_explosion = pygame.transform.scale(
                        explosion_sprite,
                        (int(explosion_sprite.get_width() * BOMB_SCALE),
                        int(explosion_sprite.get_height() * BOMB_SCALE))
                    )
                    PANTALLA.blit(scaled_explosion,
                        (bomb["x"] - camera_x - scaled_explosion.get_width()//2,
                        bomb["y"] - camera_y - scaled_explosion.get_height()//2))
                else:
                    bomb_positions[i] = None
                    state["exploding"] = False
                    state["frame"] = 0
                    
        # Filtrar las bombas que no son None antes de dibujarlas
        bomb_positions = [bomb for bomb in bomb_positions if bomb is not None]
    
    # Dibujar enemigos
    for enemy in enemy_positions:
        PANTALLA.blit(enemy["sprite"], 
                (enemy["x"] - camera_x - enemy["sprite"].get_width()//2,
                enemy["y"] - camera_y - enemy["sprite"].get_height()//2))

    # Dibujar bombas
    for bomb in bomb_positions:
        if bomb:
            PANTALLA.blit(scaled_bomb,
                        (bomb["x"] - camera_x - scaled_bomb.get_width()//2,
                        bomb["y"] - camera_y - scaled_bomb.get_height()//2))
    
    # Mostramos el sprite ya escalado
    PANTALLA.blit(scaled_current_sprite, (player_x - camera_x - scaled_current_sprite.get_width()//2, 
                                         player_y - camera_y - scaled_current_sprite.get_height()//2))
    
    # Dibujar regalos
    if taza_visible:
        PANTALLA.blit(scaled_taza,
                    (taza_position[0] - camera_x - scaled_taza.get_width()//2,
                    taza_position[1] - camera_y - scaled_taza.get_height()//2))

    if pastel_visible:
        PANTALLA.blit(scaled_pastel,
                    (pastel_position[0] - camera_x - scaled_pastel.get_width()//2,
                    pastel_position[1] - camera_y - scaled_pastel.get_height()//2))
    
    # Si se ejecutó el path finding se dibuja la línea:
    if current_path and show_path:
        draw_path(PANTALLA, current_path, camera_x, camera_y)
    else:
        show_path = False
        current_path = None
        pathfinding_active = False
    
    if current_path and len(current_path) <= 1:
        pathfinding_active = False
    
    pygame.display.flip()

# FIN BUCLE DE JUEGO #

