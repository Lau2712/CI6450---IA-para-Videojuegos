# Proyecto 3. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación de Technical Waypoints y Technical Pathfinding
import pygame, sys
from TileGraph import TileGraph
from A import pathfind_astar
from ManhattanHeuristic import ManhattanHeuristic
from DynamicArriveDecision import DynamicArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision, DisappearAction, PlayerAttackingInRangeDecision
from DynamicFleeDecision import DynamicFleeDecision
from BombAction import BombAttackAction, BombFleeAction, BombInteractionDecision
from gameMovement import handle_pathfinding_movement, handle_pathfinding_movement_exp2, handle_pathfinding_movement_player
from pygame.locals import *
import math
import random

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
Width, Height = 935, 645
PANTALLA = pygame.display.set_mode((Width,Height))

# Nombre de la ventana
pygame.display.set_caption("Stitch's Adventure")

######################################################### EDICIÓN DE LA PANTALLA ######################################################
BLANCO = (255,255,255)

# Fondo
fondo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Fondo/Fondo Original.png").convert()

# Factor de zoom
ZOOM = 1.0

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
tile_size = 30
tile_graph = TileGraph(scaled_maze, tile_size)
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
quieto = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Quieto.png")
quieto_izq = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Quieto_Izq.png")
quieto_abajo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Quieto_abajo.png")
quieto_arriba = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Quieto_arriba.png")

# Movimiento del jugador
movDerecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Corriendo_{i}.png") for i in range(1, 7)]
movIzquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Corriendo_{i}_Izq.png") for i in range(1, 7)]
movSubiendo = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Subiendo_{i}.png") for i in range(1, 7)]
movBajando = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Bajando_{i}.png") for i in range(1, 7)]
ataqueDerecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Disparar_{i}.png") for i in range(1, 6)]
ataqueIzquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Stitch/Disparar_{i}_Izq.png") for i in range(1, 6)]

# Variable para llevar la cuenta de las imágenes de los movimientos
cuentaPasos = 0

# Dirección inicial del jugador
direccion = 'derecha'
    
# Cargamos las imágenes de los enemigos
experimento1 = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Quieto_1.png")
experimento2 = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Quieto_1.png")

# Movimiento del experimento 1
movExp1Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Corriendo_{i}.png") for i in range(1, 6)]
movExp1Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Corriendo_{i}_Izq.png") for i in range(1, 6)]
ataqueExp1Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Ataque_{i}.png") for i in range(1, 5)]
ataqueExp1Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Ataque_{i}_Izq.png") for i in range(1, 5)]
desapareceExp1Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Desaparecer_{i}.png") for i in range(1, 8)]
desapareceExp1Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Desaparecer_{i}_Izq.png") for i in range(1, 8)]
muertoExp1 = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 1/Muerto_{i}.png") for i in range(1,11)]

# Movimiento del experimento 2
movExp2Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 2/Corriendo_{i}.png") for i in range(1, 7)]
movExp2Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 2/Corriendo_{i}_Izq.png") for i in range(1, 7)]
movExp2Arriba = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 2/Corriendo_{i}_Arriba.png") for i in range(1, 7)]
movExp2Abajo = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 2/Corriendo_{i}_Abajo.png") for i in range(1, 7)]
ataqueExp2Derecha = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 2/Ataque_{i}.png") for i in range(1, 8)]
ataqueExp2Izquierda = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 2/Ataque_{i}_Izq.png") for i in range(1, 8)]
muertoExp2 = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Experimento 2/Muerto_{i}.png") for i in range(1,3)]

# Velocidad de los experimentos
ENEMY_SPEED = 2.5

# Direcciones iniciales de los experimentos
enemy_directions = ['derecha', 'derecha']

# Contadores de la animación de los experimentos
enemy_animation_counters = [0, 0]

# Obstáculos
obs = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Obstaculos/Bomba.png")

# Secuencia de explosion
explosion = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Obstaculos/Explosión_{i}.png") for i in range(1, 13)]

# Premios
taza = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Obstaculos/Taza.png")
rayo = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Obstaculos/Vida_1.png")
estrellas = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Obstaculos/Estrellas_{i}.png") for i in range(1, 4)]
cofre = pygame.image.load("C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Obstaculos/Cofre.png")
pergaminos = [pygame.image.load(f"C:/Users/Usuario/Documents/Universidad/IA para videojuegos/Proyecto_3/Obstaculos/Pergaminos_{i}.png") for i in range(1, 6)]

# Variables de escalas para los jugadores/experimentos/bombas
PLAYER_SCALE = 1.2
ENEMY_SCALE = 1
BOMB_SCALE = 1
GIFTS_SCALE = 1.2

scaled_player = pygame.transform.scale(quieto,(int(quieto.get_width() * PLAYER_SCALE), int(quieto.get_height() * PLAYER_SCALE)))

# Posición del jugador en el mundo
player_x = 50
player_y = 320

scaled_experimento1 = pygame.transform.scale(experimento1,(int(experimento1.get_width() * ENEMY_SCALE),int(experimento1.get_height() * ENEMY_SCALE)))

scaled_experimento2 = pygame.transform.scale(experimento2,(int(experimento2.get_width() * ENEMY_SCALE),int(experimento2.get_height() * ENEMY_SCALE)))

scaled_bomb = pygame.transform.scale(obs,(int(obs.get_width() * BOMB_SCALE),int(obs.get_height() * BOMB_SCALE)))

scaled_taza = pygame.transform.scale(taza,(int(taza.get_width() * GIFTS_SCALE),int(taza.get_height() * GIFTS_SCALE)))
scaled_rayo = pygame.transform.scale(rayo,(int(rayo.get_width() * GIFTS_SCALE),int(rayo.get_height() * GIFTS_SCALE)))
scaled_cofre = pygame.transform.scale(cofre,(int(cofre.get_width() * GIFTS_SCALE),int(cofre.get_height() * GIFTS_SCALE)))
scaled_pergaminos = [pygame.transform.scale(pergamino,(int(pergamino.get_width() * GIFTS_SCALE),int(pergamino.get_height() * GIFTS_SCALE))) for pergamino in pergaminos]
scaled_estrella = [pygame.transform.scale(estrella,(int(estrella.get_width() * GIFTS_SCALE),int(estrella.get_height() * GIFTS_SCALE))) for estrella in estrellas]


# Posiciones y características de los experimentos
enemy_positions = [
    {"x": 400, "y": 300, "sprite": scaled_experimento1, "sprites_right": movExp1Derecha, "sprites_left": movExp1Izquierda, "sprites_up": movExp1Izquierda, "sprites_down": movExp1Izquierda, "is_attacking": False, "is_visible": True, "is_disappear": False, "in_attack_range": False, "is_dead": False, "death_animation_frame": 0, "initial_x": 400, "initial_y": 300},
    {"x": 800, "y": 80, "sprite": scaled_experimento2, "sprites_right": movExp2Derecha, "sprites_left": movExp2Izquierda, "sprites_up": movExp2Arriba, "sprites_down": movExp2Abajo, "is_attacking": False, "is_visible": True, "is_disappear": False, "in_attack_range": False, "is_dead": False, "death_animation_frame": 0, "initial_x": 800, "initial_y": 80}
]

# Posiciones de las bombas
bomb_positions = [{"x": 520, "y": 200}, {"x": 250, "y": 90}, {"x": 800, "y": 250}, {"x": 370, "y": 550},
                  {"x": 750, "y": 410}, {"x": 750, "y": 430}, {"x": 770, "y": 410}, {"x": 770, "y": 430}]

# Estados de las bombas
bomb_states = [{"exploding": False, "frame": 0} for _ in bomb_positions]

# Posiciones de los regalos
taza_position = [800, 80]
rayo_position = [650, 420]
cofre_position = [40, 320]

# Variables de los regalos
taza_visible = False
rayo_visible = True
pergamino_visible = True
current_pergamino_index = 0
collected_pergaminos = 0
TOTAL_PERGAMINOS = 5
ARRIVAL_RADIUS_GIFT = 30
ARRIVAL_RADIUS_CHEST = 35
exp1_pathfinding = False
exp2_pathfinding = False
exp1_path = None
exp2_path = None
star_visible = False
star_position = None
star_spawn_timer = 0
STAR_SPAWN_INTERVAL = 20000
STAR_EFFECT_DURATION = 10000
star_effect_active = False
star_effect_start_time = 0
NORMAL_SPEED = 1.75
BOOSTED_SPEED = 3.0

# Control de FPS
reloj = pygame.time.Clock()

# Variables de las acciones del experimento 1
DETECTION_RADIUS = 20
ARRIVAL_RADIUS = 80
MAX_SPEED = 0.5
EXP1_MIN_X = 350
EXP1_MAX_X = 620
MAX_ACCELERATION = 1.5
TARGET_RADIUS = 5.0
SLOW_RADIUS = 75.0
TIME_TO_TARGET = 1.5
exp1_following_player = True
exp1_timer = 0
exp1_INTERVAL = 20000
exp1_DURATION = 10000
exp1_last_disappear = 0
exp1_is_invisible = False 

# Variables de las acciones del experimento 2
EXP2_DETECTION_RADIUS = 10
EXP2_MIN_X = 90
EXP2_MAX_X = 1500
EXP2_PATROL_POINTS = [(180, 80), (180, 447), (400, 450), (400, 570), (600, 570), (670, 450), (820, 450), (820, 150)]
exp2_current_point_index = 0
exp2_patrol_path = None

# Variables de las acciones del jugador
BOMB_DETECTION_RADIUS = 20
BOMB_EXPLOSION_SPEED = 0.2
current_objective = "collect"
path_to_objective = None
AUTO_MOVEMENT_SPEED = 1.75
lives = 3
game_over = False
RAY_DETECTION_RADIUS = 20
RAY_AVOID_RADIUS = 30

# Variables para pathfinding
current_path = None
target_exp = None
current_sprite = quieto
PATHFINDING_SPEED = 1.5
path_flag = False

# Variables para la vida de los personajes
PLAYER_MAX_HEALTH = 100
ENEMY_MAX_HEALTH = 100
player_health = PLAYER_MAX_HEALTH
enemy1_health = ENEMY_MAX_HEALTH 
enemy2_health = ENEMY_MAX_HEALTH
last_enemy_attack_time = 0
last_player_attack_time = 0
ENEMY_ATTACK_COOLDOWN = 1000
PLAYER_ATTACK_COOLDOWN = 500

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
    
    if start_node is None:
        start_node = find_nearest_valid_node(start_x // tile_size, start_y // tile_size, tile_graph.nodes)

    if end_node is None:
        end_node = find_nearest_valid_node(end_x // tile_size, end_y // tile_size, tile_graph.nodes)
        
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
        in_zone = EXP1_MIN_X - 50 <= enemy_pos[0] <= EXP1_MAX_X + 50
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

# Función para dibujar el camino
def draw_path(screen, path, camera_x, camera_y, color):
    if path:
        # Se dibujan los nodos
        for i in range(len(path)-1):
            start = path[i].from_node
            end = path[i].to_node
            
            start_pos = (start.x * tile_size - camera_x, 
                        start.y * tile_size - camera_y)
            end_pos = (end.x * tile_size - camera_x,
                      end.y * tile_size - camera_y)
            
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

# Función para dibujar la barra de vida
def draw_health_bar(surface, x, y, width, height, current_health, max_health, border_color=(255,255,255)):
    # Make bars bigger
    width = 80
    height = 8
    
    # Calculate health percentage
    health_percentage = current_health / max_health
    
    # Draw background
    pygame.draw.rect(surface, (0,0,0), (x, y, width, height))
    
    # Determine color based on health percentage
    if health_percentage > 0.5:
        health_color = (0,255,0)  # Green
    elif health_percentage > 0.2:
        health_color = (255,165,0)  # Orange
    else:
        health_color = (255,0,0)  # Red
    
    # Calculate health width
    health_width = (current_health / max_health) * width
    
    # Draw health
    pygame.draw.rect(surface, health_color, (x, y, health_width, height))
    
    # Draw border
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)

# Función para obtener una posición válida dentro del path
def get_valid_path_position():
    while True:
        # Generate random coordinates within world bounds
        x = random.randint(220, 1650)
        y = random.randint(80, 1570)
        
        # Get the corresponding tile
        tile_x = x // tile_size 
        tile_y = y // tile_size
        
        # Check if position is in valid path tile
        tile = tile_graph.nodes.get((tile_x, tile_y))
        if tile and not check_collision(x, y):
            return [x, y]

# Función para obtener una posición válida del pergamino
def get_valid_pergamino_position():
    while True:
        # Generate random coordinates within game bounds
        x = random.randint(220, 1650)
        y = random.randint(80, 570)
        
        # Check if position is valid (not colliding with walls)
        if not check_collision(x, y):
            return [x, y]

pergamino_position = get_valid_pergamino_position()

# Función para determinar si el jugador está en el radio de ataque del enemigo
def check_player_in_attack_range(enemy_pos, player_pos, attack_radius):
    dx = player_pos[0] - enemy_pos[0]
    dy = player_pos[1] - enemy_pos[1]
    distance = math.sqrt(dx*dx + dy*dy)
    return distance <= attack_radius

# Función para generar una posición válida del star
def spawn_star():
    global star_position, star_visible
    star_position = get_valid_path_position()
    star_visible = True

# Función para mostrar la pantalla de fin del juego
def show_game_over_screen(screen, victory=False):
    # Create semi-transparent overlay
    overlay = pygame.Surface((Width, Height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0,0))
    
    # Setup font
    font = pygame.font.Font(None, 74)
    fuente = pygame.font.Font(None, 40)
    
    # Different messages for victory/defeat
    if victory:
        text = font.render("¡VICTORIA!", True, (255, 215, 0))  # Gold color
        subtext = fuente.render("¡Stitch logró recuperar todos los pergaminos!", True, (255, 255, 255))
    
    else:
        text = font.render("GAME OVER", True, (255, 0, 0))  # Red color
        subtext = font.render("Stitch ha muerto", True, (255, 255, 255))
    
    # Center the text
    text_rect = text.get_rect(center=(468, 323))
    subtext_rect = subtext.get_rect(center=(468, 350))
    
    # Draw text
    screen.blit(text, text_rect)
    screen.blit(subtext, subtext_rect)
    
    pygame.display.flip()
    
    # Wait for a moment before continuing
    pygame.time.wait(3000)

# Función para obtener un nuevo path que no pase por el rayo
def get_path_avoiding_ray(start_x, start_y, end_x, end_y, ray_pos):
    # Get normal path first
    path = get_path(start_x, start_y, end_x, end_y)
    
    if not path:
        return None
        
    # Check if path goes near ray
    for node in path:
        dx = node.from_node.x * tile_size - ray_pos[0]
        dy = node.from_node.y * tile_size - ray_pos[1] 
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < RAY_AVOID_RADIUS:
            # Path goes too close to ray, find alternative
            return find_alternative_path(start_x, start_y, end_x, end_y, ray_pos)
            
    return path

# Función para encontrar un path alternativo
def find_alternative_path(start_x, start_y, end_x, end_y, ray_pos):
    # Find intermediate waypoints to route around ray
    waypoints = []
    
    # Add waypoints in cardinal directions away from ray
    ray_x, ray_y = ray_pos
    distances = [RAY_AVOID_RADIUS * 1.5] 
    
    for angle in [0, 90, 180, 270]:
        wx = ray_x + distances[0] * math.cos(math.radians(angle))
        wy = ray_y + distances[0] * math.sin(math.radians(angle))
        
        if not check_collision(wx, wy):
            waypoints.append((wx, wy))
    
    # Try paths through each waypoint
    best_path = None
    best_length = float('inf')
    
    for wp in waypoints:
        # Get path through waypoint
        path1 = get_path(start_x, start_y, wp[0], wp[1])
        path2 = get_path(wp[0], wp[1], end_x, end_y)
        
        if path1 and path2:
            total_length = len(path1) + len(path2)
            if total_length < best_length:
                best_length = total_length
                best_path = path1 + path2
                
    return best_path

# Funciones auxiliares
def find_nearest_valid_node(x: int, y: int, nodes: dict):
    nearest_node = None
    min_distance = float('inf')
    
    for node_pos, node in nodes.items():
        distance = manhattan_distance(x, y, node_pos[0], node_pos[1])
        if distance < min_distance:
            min_distance = distance
            nearest_node = node
            
    return nearest_node

def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)

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
    new_x = player_x
    new_y = player_y

    # Velocidad de la animación
    animacion_velocidad = 0.1
    
    if current_objective == "collect" and pergamino_visible:
        if not path_to_objective:
            
            # Se valida la distancia del jugador al rayo
            dx = player_x - rayo_position[0]
            dy = player_y - rayo_position[1]
            ray_distance = math.sqrt(dx*dx + dy*dy)
            
            if ray_distance < RAY_DETECTION_RADIUS:
                # Si el rayo está en el camino se busca un nuevo path
                path_to_objective = get_path_avoiding_ray(
                    int(player_x),
                    int(player_y),
                    pergamino_position[0],
                    pergamino_position[1],
                    rayo_position
                )
            else:
                # Se obtiene el path al pergamino actual
                path_to_objective = get_path(
                int(player_x),
                int(player_y), 
                pergamino_position[0],
                pergamino_position[1]
            )
            
        old_x = new_x
        old_y = new_y
        path_player = path_to_objective
        
        if path_to_objective:
            new_x, new_y = handle_pathfinding_movement_player(
                player_x,
                player_y,
                path_to_objective,
                tile_size,
                WORLD_WIDTH,
                WORLD_HEIGHT, 
                AUTO_MOVEMENT_SPEED,
                scaled_maze
            )
            
            if not check_collision(new_x, new_y):
                player_x = new_x
                player_y = new_y
                
                # Update animation direction
                dx = player_x - old_x
                dy = player_y - old_y
                
                if abs(dx) > abs(dy):
                    direccion = 'derecha' if dx > 0 else 'izquierda'
                    current_sprite = movDerecha[int(cuentaPasos)] if dx > 0 else movIzquierda[int(cuentaPasos)]
                else:
                    direccion = 'arriba' if dy < 0 else 'abajo'
                    current_sprite = movSubiendo[int(cuentaPasos)] if dy < 0 else movBajando[int(cuentaPasos)]
                
                cuentaPasos = (cuentaPasos + 0.2) % len(movDerecha)

    elif current_objective == "return":
        if not path_to_objective:
            # Se obtiene el path al cofre
            path_to_objective = get_path(
                int(player_x),
                int(player_y),
                cofre_position[0],
                cofre_position[1]
            )
        
        path_player = path_to_objective
        
        if path_to_objective:
            new_x, new_y = handle_pathfinding_movement_player(
                player_x,
                player_y,
                path_to_objective,
                tile_size,
                WORLD_WIDTH,
                WORLD_HEIGHT,
                AUTO_MOVEMENT_SPEED,
                scaled_maze
            )
            
            if not check_collision(new_x, new_y):
                player_x = new_x
                player_y = new_y
                
                # Update animación
                dx = new_x - player_x
                dy = new_y - player_y
                
                if abs(dx) > abs(dy):
                    direccion = 'derecha' if dx > 0 else 'izquierda'
                    current_sprite = movDerecha[int(cuentaPasos)] if dx > 0 else movIzquierda[int(cuentaPasos)]
                else:
                    direccion = 'arriba' if dy < 0 else 'abajo'
                    current_sprite = movSubiendo[int(cuentaPasos)] if dy < 0 else movBajando[int(cuentaPasos)]
                
                cuentaPasos = (cuentaPasos + 0.2) % len(movDerecha)
    
    # Si el jugador ya alcanzó el pergamino, cambia el objetico
    if pergamino_visible and pergamino_position:
        dx = player_x - pergamino_position[0]
        dy = player_y - pergamino_position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance <= ARRIVAL_RADIUS_GIFT:
            # Se cambia el objetivo a retornar al cofre
            current_objective = "return"
            path_to_objective = None
            pergamino_visible = False

    # Variables de posición del cofre vs jugador
    dx_chest = player_x - cofre_position[0]
    dy_chest = player_y - cofre_position[1]
    distance_to_chest = math.sqrt(dx_chest*dx_chest + dy_chest*dy_chest)

    # Si el jugador llegó al cofre, se incrementa el número de pergaminos
    if current_objective == "return" and distance_to_chest <= ARRIVAL_RADIUS_CHEST:
        collected_pergaminos += 1
        pergamino_visible = True
        
        if collected_pergaminos < TOTAL_PERGAMINOS:
            # Solo se genera un nuevo pergamino después de entregar el actual al cofre
            pergamino_position = get_valid_pergamino_position()
            current_pergamino_index += 1
            current_objective = "collect"
            path_to_objective = None
        else:
            # Si se recolectaron todos los pergaminos
            pergamino_visible = False
            pergamino_position = None

    # Se escala la imagen del sprite actual
    scaled_current_sprite = pygame.transform.scale(current_sprite,(int(current_sprite.get_width() * PLAYER_SCALE),int(current_sprite.get_height() * PLAYER_SCALE)))

    # Verificar colisiones antes de actualizar la posición
    if not check_collision(new_x, new_y):
        player_x = new_x
        player_y = new_y
    
    # Limitar al jugador dentro del mundo
    player_x = max(scaled_player.get_width()//2, min(WORLD_WIDTH - scaled_player.get_width()//2, player_x))
    player_y = max(scaled_player.get_height()//2, min(WORLD_HEIGHT - scaled_player.get_height()//2, player_y))
    
    # # Actualizar la cámara
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
        # Verificar si el jugador está en el radio de ataque del enemigo
        enemy["in_attack_range"] = check_player_in_attack_range(
            (enemy["x"], enemy["y"]), 
            (player_x, player_y),
            ARRIVAL_RADIUS
        )
        
        # Si está en el radio se activa la animación
        if enemy["in_attack_range"] and not enemy["is_disappear"]:
            enemy["is_attacking"] = True
            enemy_animation_counters[i] += 0.1
            
            # Seleccionamos el sprite según el enemigo
            if i == 0:
                attack_sprites = ataqueExp1Derecha if enemy_directions[i] == 'derecha' else ataqueExp1Izquierda
            else:
                attack_sprites = ataqueExp2Derecha if enemy_directions[i] == 'derecha' else ataqueExp2Izquierda
            
            if enemy_animation_counters[i] >= len(attack_sprites):
                enemy_animation_counters[i] = 0
                
            current_frame = int(enemy_animation_counters[i])
            enemy["sprite"] = pygame.transform.scale(
                attack_sprites[current_frame],
                (int(attack_sprites[current_frame].get_width() * ENEMY_SCALE),
                int(attack_sprites[current_frame].get_height() * ENEMY_SCALE))
            )
            
            # Aplicar daño al jugador
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_attack_time >= ENEMY_ATTACK_COOLDOWN:
                player_health -= 10
                player_health = max(0, player_health)
                last_enemy_attack_time = current_time
        
        else:
            enemy["is_attacking"] = False
        
        if i == 0:
            current_time_exp1 = pygame.time.get_ticks()
            
            if enemy1_health <= 0 and not enemy_positions[i]["is_dead"]:
                enemy_positions[i]["is_dead"] = True
                enemy_positions[i]["death_animation_frame"] = 0
                
            if enemy_positions[i]["is_dead"]:
                # Animación de muerte
                enemy_positions[i]["death_animation_frame"] += 0.1
                current_frame_exp1 = int(current_frame + enemy_positions[i]["death_animation_frame"])
            
                if current_frame_exp1 < len(muertoExp1):
                    enemy_positions[i]["sprite"] = pygame.transform.scale(
                        muertoExp1[current_frame_exp1],
                        (int(muertoExp1[current_frame_exp1].get_width() * ENEMY_SCALE),
                        int(muertoExp1[current_frame_exp1].get_height() * ENEMY_SCALE))
                    )
            
                else:
                    # Reinicio
                    enemy_positions[i]["x"] = enemy_positions[i]["initial_x"]
                    enemy_positions[i]["y"] = enemy_positions[i]["initial_y"]
                    enemy1_health = ENEMY_MAX_HEALTH
                    enemy_positions[i]["is_dead"] = False
                    enemy_positions[i]["is_attacking"] = False
                    enemy_positions[i]["is_disappear"] = False
                    enemy_positions[i]["is_visible"] = True
                    exp1_following_player = True
            
            if enemy1_health <= ENEMY_MAX_HEALTH * 0.2 and enemy1_health > 0:
                if not exp1_is_invisible and current_time - exp1_last_disappear >= exp1_INTERVAL:
                    enemy["is_disappear"] = True
                    exp1_is_invisible = True
                    exp1_timer = current_time
        
            if exp1_is_invisible:
                # Update animación
                enemy_animation_counters[i] += 0.1
                sprites = desapareceExp1Derecha if dx > 0 else desapareceExp1Izquierda
                
                if enemy_animation_counters[i] >= len(sprites):
                    enemy_animation_counters[i] = 0
                    
                current_frame = int(enemy_animation_counters[i])
                enemy["sprite"] = pygame.transform.scale(
                    sprites[current_frame],
                    (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(sprites[current_frame].get_height() * ENEMY_SCALE))
                )
                
                if current_time - exp1_timer >= exp1_DURATION:
                    enemy["is_disappear"] = False
                    exp1_is_invisible = False
                    exp1_last_disappear = current_time
            
            if enemy1_health > ENEMY_MAX_HEALTH * 0.2:    
                if exp1_following_player:
                    
                    if star_effect_active:
                        pass
                    else:
                        
                        # Se obtiene el path al jugador
                        exp1_path = get_path(
                            int(enemy["x"]), 
                            int(enemy["y"]),
                            int(player_x),
                            int(player_y)
                        )
                        
                        if exp1_path:
                            dx = player_x - enemy["x"]
                            dy = player_y - enemy["y"]
                            distance = math.sqrt(dx*dx + dy*dy)

                            if distance <= DETECTION_RADIUS and enemy["in_attack_range"]:
                                # Animación de ataque
                                enemy["is_attacking"] = True
                                enemy_animation_counters[i] += 0.1
                                attack_sprites = ataqueExp1Derecha if enemy_directions[i] == 'derecha' else ataqueExp1Izquierda
                                
                                if enemy_animation_counters[i] >= len(attack_sprites):
                                    enemy_animation_counters[i] = 0
                                    enemy["is_attacking"] = False
                                
                                current_frame = int(enemy_animation_counters[i])
                                if current_frame < len(attack_sprites):
                                    enemy["sprite"] = pygame.transform.scale(
                                        attack_sprites[current_frame],
                                        (int(attack_sprites[current_frame].get_width() * ENEMY_SCALE),
                                        int(attack_sprites[current_frame].get_height() * ENEMY_SCALE))
                                    )
                            else:
                                new_x_exp1, new_y_exp1 = handle_pathfinding_movement(
                                    enemy["x"],
                                    enemy["y"],
                                    exp1_path,
                                    tile_size, 
                                    WORLD_WIDTH,
                                    WORLD_HEIGHT,
                                    PATHFINDING_SPEED,
                                    scaled_maze
                                )
                                
                                if not check_collision(new_x_exp1, new_y_exp1):
                                    enemy["x"] = new_x_exp1 
                                    enemy["y"] = new_y_exp1
                                    
                                    dx = new_x_exp1 - enemy["x"]
                                    enemy_directions[i] = 'derecha' if dx > 0 else 'izquierda'
                                    
                                    # Update animación
                                    enemy_animation_counters[i] += 0.1
                                    sprites = movExp1Derecha if dx > 0 else movExp1Izquierda
                                    
                                    if enemy_animation_counters[i] >= len(sprites):
                                        enemy_animation_counters[i] = 0
                                        
                                    current_frame = int(enemy_animation_counters[i])
                                    enemy["sprite"] = pygame.transform.scale(
                                        sprites[current_frame],
                                        (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                                        int(sprites[current_frame].get_height() * ENEMY_SCALE))
                                    )
                                else:
                                    if not check_collision(new_x, enemy["y"] - ENEMY_SPEED):
                                        enemy["y"] -= ENEMY_SPEED
                                    elif not check_collision(new_x, enemy["y"] + ENEMY_SPEED):
                                        enemy["y"] += ENEMY_SPEED
                        
                else:
                    # Definimos las acciones del experimento 1
                    # Dynamic Arrive
                    dynamic_action = DynamicArriveAction(enemy, (player_x, player_y), MAX_SPEED, MAX_ACCELERATION, TARGET_RADIUS, SLOW_RADIUS, TIME_TO_TARGET)
                    # Ataque
                    attack_action = AttackAction(enemy, enemy_directions[i], ataqueExp1Derecha, ataqueExp1Izquierda)
                    # Desaparecer
                    disappear_action = DisappearAction(enemy, enemy_directions[i],desapareceExp1Derecha,desapareceExp1Izquierda)
                    
                    # Se determina la decisión de patrullar o aplicar dynamic
                    chase_decision = InRangeDecision((enemy["x"], enemy["y"]),(player_x, player_y),dynamic_action,patrol_action,test_player_in_range_and_zone_exp1)
                    
                    # Se determina la decision de atacar
                    attack_decision = PlayerReachedDecision((enemy["x"], enemy["y"]),(player_x, player_y),attack_action,chase_decision,ARRIVAL_RADIUS)
                    
                    # Se determina la decisión de desaparecer
                    disappear_decision = PlayerAttackingInRangeDecision((enemy["x"], enemy["y"]),(player_x, player_y), enemy["in_attack_range"],DETECTION_RADIUS,disappear_action,attack_decision)
                    
                    # Variable acción para determinar que se va a realizar
                    action = disappear_decision.make_decision()
            
            
        # Experimento 2
        else:
            if enemy2_health <= 0  and not enemy_positions[i]["is_dead"]:
                enemy_positions[i]["is_dead"] = True
                enemy_positions[i]["death_animation_frame"] = 0
                
            if enemy_positions[i]["is_dead"]:
                # Play death animation
                enemy_positions[i]["death_animation_frame"] += 0.1
                current_frame = int(enemy_positions[i]["death_animation_frame"])
                
                if current_frame < len(muertoExp2):
                    enemy_positions[i]["sprite"] = pygame.transform.scale(
                        muertoExp2[current_frame],
                        (int(muertoExp2[current_frame].get_width() * ENEMY_SCALE),
                        int(muertoExp2[current_frame].get_height() * ENEMY_SCALE))
                    )
                else:
                    # Reinicio
                    enemy_positions[i]["x"] = enemy_positions[i]["initial_x"]
                    enemy_positions[i]["y"] = enemy_positions[i]["initial_y"]
                    enemy2_health = ENEMY_MAX_HEALTH
                    enemy_positions[i]["is_dead"] = False
                    enemy_positions[i]["is_attacking"] = False
                    enemy_positions[i]["is_visible"] = True
                    exp2_current_point_index = 0
                    exp2_patrol_path = None
            
            if enemy2_health <= ENEMY_MAX_HEALTH * 0.2 and enemy2_health > 0:
                taza_visible = True
                
                # Se obtiene el path a la taza
                forward_path = get_experiment_path(enemy_positions[1]["x"], enemy_positions[1]["y"], taza_position[0], taza_position[1])
                
                # Se obtiene el path de regreso
                return_path = get_experiment_path(enemy_positions[1]["x"], enemy_positions[1]["y"], 
                                                enemy_positions[1]["x"], enemy_positions[1]["y"])
                
                # Se compara el tamaño de los paths para determinar el más eficiente
                if forward_path and return_path:
                    
                    if len(return_path) < len(forward_path):
                        exp2_path = return_path
                    else:
                        exp2_path = forward_path
                        
                elif forward_path:
                    exp2_path = forward_path
                    
                elif return_path:
                    exp2_path = return_path
                    
                exp2_pathfinding = True

                if exp2_pathfinding and exp2_path:
                    new_x_exp2, new_y_exp2 = handle_pathfinding_movement_exp2(
                        enemy_positions[1]["x"],
                        enemy_positions[1]["y"],
                        exp2_path, 
                        tile_size,
                        WORLD_WIDTH,
                        WORLD_HEIGHT,
                        PATHFINDING_SPEED
                    )
                    
                    # Verificar si el enemigo ha llegado a la taza
                    dx_cup = taza_position[0] - enemy_positions[1]["x"]
                    dy_cup = taza_position[1] - enemy_positions[1]["y"]
                    distance_to_cup = math.sqrt(dx_cup*dx_cup + dy_cup*dy_cup)
                    
                    if distance_to_cup < ARRIVAL_RADIUS_GIFT:
                        # Recargar vida
                        enemy2_health = ENEMY_MAX_HEALTH
                        taza_visible = False
                        
                        # Reseteamos pathfinding
                        exp2_pathfinding = False
                        exp2_path = None
                        
                        # Retornamos al comportamiento normal
                        exp2_current_point_index = 0
                        exp2_patrol_path = None
                    
                    if not check_collision(new_x_exp2, new_y_exp2):
                        # Update posición
                        enemy_positions[1]["x"] = new_x_exp2
                        enemy_positions[1]["y"] = new_y_exp2
                        
                        if abs(new_x_exp2) > abs(new_y_exp2):
                            enemy_directions[1] = 'derecha' if new_x_exp2 > 0 else 'izquierda'
                            sprites = enemy_positions[1]["sprites_right"] if new_x_exp2 > 0 else enemy_positions[1]["sprites_left"]
                        else:
                            enemy_directions[1] = 'arriba' if new_y_exp2 < 0 else 'abajo'
                            sprites = enemy_positions[1]["sprites_up"] if new_y_exp2 < 0 else enemy_positions[1]["sprites_down"]
                        
                        # Update animación
                        enemy_animation_counters[1] += 0.1
                        if enemy_animation_counters[1] >= len(sprites):
                            enemy_animation_counters[1] = 0
                            
                        current_frame = int(enemy_animation_counters[1])
                        enemy_positions[1]["sprite"] = pygame.transform.scale(
                            sprites[current_frame],
                            (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                            int(sprites[current_frame].get_height() * ENEMY_SCALE))
                        )
            
            else:
                if star_effect_active:
                    pass
                else:
                    taza_visible = False
                    
                    # Definimos las acciones del experimento 2
                    patrol_action = PatrolAction(enemy, enemy_directions[i])
                    
                    # Árbol de decisión
                    attack_action = AttackAction(enemy, enemy_directions[i], ataqueExp2Derecha, ataqueExp2Izquierda)
                    decision_tree = DynamicFleeDecision(enemy, (player_x, player_y), enemy["in_attack_range"], EXP2_DETECTION_RADIUS, attack_action, patrol_action, EXP2_MIN_X, EXP2_MAX_X)
                    
                    # Determinar acción
                    action = decision_tree.make_decision()
                    if action == "attack":
                        enemy["is_attacking"] = True
                        enemy_animation_counters[i] += 0.1
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
                        
                        # Obtenemos el punto de destino
                        current_target = EXP2_PATROL_POINTS[exp2_current_point_index]
                        
                        # Obtenemos o actualizamos el path al punto de destino
                        if not exp2_patrol_path:
                            exp2_patrol_path = get_path(
                                int(enemy["x"]), 
                                int(enemy["y"]),
                                current_target[0],
                                current_target[1]
                            )
                        
                        # Nos movemos por el path
                        if exp2_patrol_path:
                            new_x, new_y = handle_pathfinding_movement_exp2(
                                enemy["x"],
                                enemy["y"],
                                exp2_patrol_path,
                                tile_size,
                                WORLD_WIDTH, 
                                WORLD_HEIGHT,
                                ENEMY_SPEED,
                            )
                            
                            if not check_collision(new_x, new_y):
                                dx = new_x - enemy["x"]
                                dy = new_y - enemy["y"]
                                
                                # Update posición
                                enemy["x"] = new_x
                                enemy["y"] = new_y
                                
                                if abs(dx) > abs(dy):
                                    enemy_directions[i] = 'derecha' if dx > 0 else 'izquierda'
                                    sprites = enemy["sprites_right"] if dx > 0 else enemy["sprites_left"]
                                    
                                else: 
                                    enemy_directions[i] = 'arriba' if dy < 0 else 'abajo'
                                    sprites = enemy["sprites_up"] if dy < 0 else enemy["sprites_down"]
                                
                                # Update animación
                                enemy_animation_counters[i] += 0.1
                                
                                if enemy_animation_counters[i] >= len(sprites):
                                    enemy_animation_counters[i] = 0
                                    
                                current_frame_exp2 = int(enemy_animation_counters[i])
                                enemy["sprite"] = pygame.transform.scale(
                                    sprites[current_frame_exp2],
                                    (int(sprites[current_frame_exp2].get_width() * ENEMY_SCALE),
                                    int(sprites[current_frame_exp2].get_height() * ENEMY_SCALE))
                                )
                                
                                # Verificar si se ha llegado al punto de destino
                                dx_1 = current_target[0] - enemy["x"]
                                dy_1 = current_target[1] - enemy["y"]
                                if math.sqrt(dx_1*dx_1 + dy_1*dy_1) < ARRIVAL_RADIUS:
                                    exp2_current_point_index = (exp2_current_point_index + 1) % len(EXP2_PATROL_POINTS)
                                    exp2_patrol_path = None

                    else:
                        enemy["is_attacking"] = False
                        if enemy_directions[i] == 'derecha':
                            new_x = action.enemy["x"] + ENEMY_SPEED
                            
                            if new_x > EXP2_MAX_X:
                                enemy_directions[i] = 'izquierda'
                        else:
                            new_x = enemy["x"] - ENEMY_SPEED
                            if new_x < EXP2_MIN_X:
                                enemy_directions[i] = 'derecha'
                                
                        enemy["x"] = new_x
            
        # Actualizar animación
        if enemy["is_attacking"]:
            current_time = pygame.time.get_ticks()
            dx = player_x - enemy["x"]
            dy = player_y - enemy["y"]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= DETECTION_RADIUS and current_time - last_enemy_attack_time >= ENEMY_ATTACK_COOLDOWN:
                player_health -= 10
                player_health = max(0, player_health)
                last_enemy_attack_time = current_time

        if not enemy["is_attacking"] and not enemy["is_disappear"] :
            enemy_animation_counters[i] += 0.1
            if enemy_directions[i] == 'derecha':
                sprites = enemy["sprites_right"]
            elif enemy_directions[i] == 'izquierda':
                sprites = enemy["sprites_left"]
            elif enemy_directions[i] == 'arriba':
                sprites = enemy["sprites_up"]
            elif enemy_directions[i] == 'abajo':
                sprites = enemy["sprites_down"]
            
            if enemy_animation_counters[i] >= len(sprites):
                enemy_animation_counters[i] = 0
                
            current_frame = int(enemy_animation_counters[i])
            enemy["sprite"] = pygame.transform.scale(
                sprites[current_frame],
                (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                int(sprites[current_frame].get_height() * ENEMY_SCALE))
            )

        if enemy["in_attack_range"] and not enemy["is_disappear"]:
            enemy["is_attacking"] = True
            
            # Update animación del ataque
            cuentaPasos = (cuentaPasos + animacion_velocidad) % len(ataqueDerecha)

            if direccion == 'derecha':
                current_sprite = ataqueDerecha[int(cuentaPasos)]
            else:
                current_sprite = ataqueIzquierda[int(cuentaPasos)]

            scaled_current_sprite = pygame.transform.scale(
                current_sprite,
                (int(current_sprite.get_width() * PLAYER_SCALE),
                int(current_sprite.get_height() * PLAYER_SCALE))
            )
            
            # Applicar daño al jugador
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_attack_time >= ENEMY_ATTACK_COOLDOWN:
                player_health -= 10
                player_health = max(0, player_health)
                last_enemy_attack_time = current_time
            
            if current_time - last_player_attack_time >= PLAYER_ATTACK_COOLDOWN:
                if i == 0:
                    enemy1_health -= 12
                    enemy1_health = max(0, enemy1_health)
                else: 
                    enemy2_health -= 12
                    enemy2_health = max(0, enemy2_health)
                last_player_attack_time = current_time
        
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

                # Definimos el árbol de decisión
                bomb_decision = BombInteractionDecision((player_x, player_y), bomb_positions, BOMB_DETECTION_RADIUS, bomb_attack)

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
                        new_x = player_x + steering.linear.x
                        new_y = player_y + steering.linear.z
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
    
    # Lógica estrella de poder
    current_time = pygame.time.get_ticks()

    if not star_visible and current_time - star_spawn_timer >= STAR_SPAWN_INTERVAL:
        spawn_star()
        star_spawn_timer = current_time

    # Si el jugador alcanzó la estrella
    if star_visible and star_position:
        dx = player_x - star_position[0]
        dy = player_y - star_position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if path_flag == False:
            old_path = path_player
            old_star_path = []
            combined_path = []
        
        # Update path
        if path_to_objective:
            path_to_objective = get_path(player_x, player_y, star_position[0], star_position[1])
            
            if path_flag == False:
                old_star_path = path_to_objective
                
                # Update path para dibujar
                if current_objective == "collect":
                    path_aux = get_path(star_position[0], star_position[1], pergamino_position[0], pergamino_position[1])
                else:
                    path_aux = get_path(star_position[0], star_position[1], cofre_position[0], cofre_position[1])
                
                combined_path = old_star_path + path_aux
                path_flag = True
            
            # Tactical path
            draw_path(PANTALLA, combined_path, camera_x, camera_y, (255, 0, 0))
            # Normal path
            draw_path(PANTALLA, old_path, camera_x, camera_y, (0, 0, 255))
        
        if distance <= ARRIVAL_RADIUS_GIFT:
            star_visible = False
            star_effect_active = True
            star_effect_start_time = current_time
            
            # Update path
            if current_objective == "collect":
                path_to_objective = get_path(player_x, player_y, pergamino_position[0], pergamino_position[1])
            else:
                path_to_objective = get_path(player_x, player_y, cofre_position[0], cofre_position[1])
            
            path_flag = False

    # Duración del poder de la estrella
    if star_effect_active:
        if current_time - star_effect_start_time >= STAR_EFFECT_DURATION:
            star_effect_active = False
            AUTO_MOVEMENT_SPEED = NORMAL_SPEED
        else:
            AUTO_MOVEMENT_SPEED = BOOSTED_SPEED
    
    # Condiciones para finalizar el juego
    if player_health <= 0:
        lives -= 1
        if lives <= 0:
            show_game_over_screen(PANTALLA, victory=False)
            game_over = True
        else:
            # Resetear al jugador
            player_health = PLAYER_MAX_HEALTH
            AUTO_MOVEMENT_SPEED = 1.75
            star_effect_active = False
            star_effect_start_time = 0
            star_visible = False
            player_x = 50
            player_y = 310

    # Condición victoria
    if collected_pergaminos >= TOTAL_PERGAMINOS:
        show_game_over_screen(PANTALLA, victory=True)
        game_over = True
    
    if game_over:
        pygame.quit()
        sys.exit()
    
    # Dibujar enemigos
    for enemy in enemy_positions:
        PANTALLA.blit(enemy["sprite"], 
                (enemy["x"] - camera_x - enemy["sprite"].get_width()//2,
                enemy["y"] - camera_y - enemy["sprite"].get_height()//2))

    # Dibujar bombas
    for bomb in bomb_positions:
        if bomb is not None:
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
    
    PANTALLA.blit(scaled_rayo,
                (rayo_position[0] - camera_x - scaled_rayo.get_width()//2,
                rayo_position[1] - camera_y - scaled_rayo.get_height()//2))
    
    # Si la estrella es visible
    if star_visible and star_position:
        current_star_frame = int((pygame.time.get_ticks() // 200) % len(scaled_estrella))
        PANTALLA.blit(scaled_estrella[current_star_frame],
                    (star_position[0] - camera_x - scaled_estrella[current_star_frame].get_width()//2,
                    star_position[1] - camera_y - scaled_estrella[current_star_frame].get_height()//2))
    
    # Pergamino visible
    if pergamino_visible and pergamino_position is None:
        pergamino_position = get_valid_pergamino_position()

    # Se verifica si el jugador ha coleccionado el pergamino
    if pergamino_visible and pergamino_position:
        
        scaled_pergamino = pygame.transform.scale(
            pergaminos[current_pergamino_index],
            (int(pergaminos[current_pergamino_index].get_width() * GIFTS_SCALE),
            int(pergaminos[current_pergamino_index].get_height() * GIFTS_SCALE))
        )
        PANTALLA.blit(scaled_pergamino,
                    (pergamino_position[0] - camera_x - scaled_pergamino.get_width()//2,
                     pergamino_position[1] - camera_y - scaled_pergamino.get_height()//2))
        
        dx = player_x - pergamino_position[0]
        dy = player_y - pergamino_position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance <= ARRIVAL_RADIUS_GIFT:
            collected_pergaminos += 1
            
            if collected_pergaminos < TOTAL_PERGAMINOS:
                # Nueva posición para el siguiente pergamino
                pergamino_position = get_valid_pergamino_position()
                current_pergamino_index += 1
            else:
                # todos los pergaminos recolectados
                pergamino_visible = False
                pergamino_position = None
    
    # Dibujar cofre
    PANTALLA.blit(scaled_cofre,
                (cofre_position[0] - camera_x - scaled_cofre.get_width()//2,
                cofre_position[1] - camera_y - scaled_cofre.get_height()//2))

    # Barras de vida
    # Jugador
    draw_health_bar(PANTALLA, player_x - camera_x - 50, player_y - camera_y - 40, 100, 10, player_health, PLAYER_MAX_HEALTH)

    # Experimento 1
    draw_health_bar(PANTALLA, enemy_positions[0]["x"] - camera_x - 50, enemy_positions[0]["y"] - camera_y - 40, 100, 10, enemy1_health,ENEMY_MAX_HEALTH)

    # Experimento 2
    draw_health_bar(PANTALLA, enemy_positions[1]["x"] - camera_x - 50, enemy_positions[1]["y"] - camera_y - 40, 100, 10, enemy2_health, ENEMY_MAX_HEALTH)

    pygame.display.flip()

# FIN BUCLE DE JUEGO #

