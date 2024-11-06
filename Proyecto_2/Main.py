# Proyecto 2. Inteligencia Artificial para Videojuegos
# Autor: Laura León 17-10307

# Implementación de los algoritmos World Representation y Toma de Decisiones
import pygame, sys
from TileGraph import TileGraph
from A import pathfind_astar
from KinematicArrive import KinematicArrive
from KinematicFlee import KinematicFlee
from ManhattanHeuristic import ManhattanHeuristic
from KinematicArriveDecision import KinematicArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision
from KinematicFleeDecision import KinematicFleeAction, KinematicFleeDecision, Exp2AttackAction, PlayerAttackingDecision
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


# Variables de escalas para los jugadores/experimentos/bombas
PLAYER_SCALE = 1.5
ENEMY_SCALE = 1.2
BOMB_SCALE = 1.5

scaled_player = pygame.transform.scale(
    quieto,
    (int(quieto.get_width() * PLAYER_SCALE),
     int(quieto.get_height() * PLAYER_SCALE))
)

# Posición del jugador en el mundo
player_x = 0
player_y = 700 

scaled_experimento1 = pygame.transform.scale(
    experimento1,
    (int(experimento1.get_width() * ENEMY_SCALE),
     int(experimento1.get_height() * ENEMY_SCALE))
)

scaled_experimento2 = pygame.transform.scale(
    experimento2,
    (int(experimento2.get_width() * ENEMY_SCALE),
     int(experimento2.get_height() * ENEMY_SCALE))
)

scaled_bomb = pygame.transform.scale(
    obs,
    (int(obs.get_width() * BOMB_SCALE),
     int(obs.get_height() * BOMB_SCALE))
)

# Posiciones de los experimentos
enemy_positions = [
    {"x": 1000, "y": 650, "sprite": scaled_experimento1, "sprites_right": movExp1Derecha, "sprites_left": movExp1Izquierda, "is_attacking": False},
    {"x": 1300, "y": 200, "sprite": scaled_experimento2, "sprites_right": movExp2Derecha, "sprites_left": movExp2Izquierda, "is_attacking": False}
]

# Posiciones de las bombas
bomb_positions = [
    {"x": 900, "y": 1200},
    {"x": 1650, "y": 600},
    {"x": 1075, "y": 450},
    {"x": 500, "y": 200}
]
bomb_states = [{"exploding": False, "frame": 0} for _ in bomb_positions]
exp2_fleeing = False

# Control de FPS
reloj = pygame.time.Clock()

# Variables de las acciones del experimento 1
DETECTION_RADIUS = 100
ARRIVAL_RADIUS = 30
MAX_SPEED = 4
EXP1_MIN_X = 850
EXP1_MAX_X = 1150

# Variables de las acciones del experimento 2
EXP2_DETECTION_RADIUS = 100
EXP2_FLEE_SPEED = 5
EXP2_MIN_X = 400
EXP2_MAX_X = 1650

# Variables de las acciones del jugador
BOMB_DETECTION_RADIUS = 80
BOMB_EXPLOSION_SPEED = 0.2

# Variables para pathfinding
current_path = None
target_exp = None
current_sprite = quieto

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

# Función para decidir el comportamiento del experimento 1
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

def test_player_in_range_and_zone_exp2(enemy_pos, player_pos):
    dx = player_pos[0] - enemy_pos[0]
    dy = player_pos[1] - enemy_pos[1]
    distance = math.sqrt(dx*dx + dy*dy)
    
    # Detectamos si el jugador está dentro del radio de detección
    in_range = distance <= EXP2_DETECTION_RADIUS
    
    # Se expande el área cuando se persigue al jugador
    if in_range:
        in_zone = EXP2_MIN_X - 100 <= enemy_pos[0] <= EXP2_MAX_X + 100
    else:
        in_zone = EXP2_MIN_X <= enemy_pos[0] <= EXP2_MAX_X
    
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
        cuentaPasos += animacion_velocidad
        if cuentaPasos >= len(movSubiendo):
            cuentaPasos = 0
        current_sprite = movSubiendo[int(cuentaPasos)]
        
    elif keys[pygame.K_DOWN]:
        new_y += MOVE_SPEED
        cuentaPasos += animacion_velocidad
        if cuentaPasos >= len(movBajando):
            cuentaPasos = 0
        current_sprite = movBajando[int(cuentaPasos)]
        
    elif keys[pygame.K_SPACE]:
        show_path = True
        current_path, target_exp = encontrar_experimento_cercano(player_x, player_y, enemy_positions)
        
        # Se acerca al experimento más cercano
        current_path, target_exp = encontrar_experimento_cercano(
            player_x, player_y, enemy_positions
        )

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
    
    else:
        show_path = False
        current_path = None
        cuentaPasos = 0
        current_sprite = quieto if direccion == 'derecha' else quieto_izq

    # Se escala la imagen del sprite actual
    scaled_current_sprite = pygame.transform.scale(
        current_sprite,
        (int(current_sprite.get_width() * PLAYER_SCALE),
         int(current_sprite.get_height() * PLAYER_SCALE))
    )

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
    
    # Mostramos el sprite ya escalado
    PANTALLA.blit(scaled_current_sprite, (player_x - camera_x - scaled_current_sprite.get_width()//2, 
                                         player_y - camera_y - scaled_current_sprite.get_height()//2))
    
    # Actualizamos la posición y animación de los experimientos
    for i, enemy in enumerate(enemy_positions):
        if i == 0:
            # Utilizamos KinematicArrive para realizar el movimiento de acercarse al jugador
            kinematic_action = KinematicArriveAction(enemy, (player_x, player_y), MAX_SPEED, ARRIVAL_RADIUS)
            patrol_action = PatrolAction(enemy, enemy_directions[i])
            
            # Se determina la decisión
            chase_decision = InRangeDecision(
                (enemy["x"], enemy["y"]),
                (player_x, player_y),
                kinematic_action,
                patrol_action,
                test_player_in_range_and_zone_exp1
            )
            
            attack_action = AttackAction(enemy, enemy_directions[i], ataqueExp1Derecha, ataqueExp1Izquierda)
            attack_decision = PlayerReachedDecision(
                (enemy["x"], enemy["y"]),
                (player_x, player_y),
                attack_action,
                chase_decision,
                ARRIVAL_RADIUS
            )
            
            action = attack_decision.make_decision()

            if action == "attack":
                enemy["is_attacking"] = True
                enemy_animation_counters[i] += 0.2
                attack_sprites = ataqueExp1Derecha if enemy_directions[i] == 'derecha' else ataqueExp1Izquierda
                
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

            elif isinstance(action, KinematicArrive):
                enemy["is_attacking"] = False
                steering = action.getSteering()
                if steering:
                    new_x = enemy["x"] + steering.velocity.x
                    enemy["x"] = new_x
                    enemy_directions[i] = 'derecha' if steering.velocity.x > 0 else 'izquierda'
                    
            elif action == "patrol":
                enemy["is_attacking"] = False
                # Comportamiento de patrulla
                if enemy_directions[i] == 'derecha':
                    new_x = enemy["x"] + ENEMY_SPEED
                else:
                    new_x = enemy["x"] - ENEMY_SPEED
                
                if check_collision(new_x, enemy["y"]):
                    enemy_directions[i] = 'izquierda' if enemy_directions[i] == 'derecha' else 'derecha'
                else:
                    enemy["x"] = new_x
        # Experimento 2
        else:
            # En la sección donde manejas el Experimento 2
            kinematic_flee = KinematicFleeAction(
                enemy,
                (player_x, player_y),
                EXP2_FLEE_SPEED,
                EXP2_DETECTION_RADIUS,
                WORLD_WIDTH,
                WORLD_HEIGHT,
                EXP2_MIN_X,
                EXP2_MAX_X
            )
            
            attack_action = Exp2AttackAction(
                enemy, 
                enemy_directions[i],
                ataqueExp2Derecha,
                ataqueExp2Izquierda
            )

            patrol_action = PatrolAction(enemy, enemy_directions[i])
            
            player_is_attacking = keys[pygame.K_x]
            
            decision_tree = KinematicFleeDecision(
                enemy,
                (player_x, player_y),
                player_is_attacking,
                EXP2_DETECTION_RADIUS,
                kinematic_flee,
                attack_action,
                patrol_action,
                EXP2_MIN_X,
                EXP2_MAX_X
            )

            action = decision_tree.make_decision()
            print(f"Action type: {type(action)}")
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
                # Comportamiento de patrulla
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
                
        # Actualizar animación
        if not enemy["is_attacking"]:
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
    
    # Lógica de explosión de las bombas
    for i, bomb in enumerate(bomb_positions):
        if not bomb_states[i]["exploding"]:
            # Calculamos la distancia entre la bomba y el jugador
            dx = player_x - bomb["x"]
            dy = player_y - bomb["y"]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= BOMB_DETECTION_RADIUS:
                bomb_states[i]["exploding"] = True
                
        if bomb_states[i]["exploding"]:
            bomb_states[i]["frame"] += BOMB_EXPLOSION_SPEED
            if bomb_states[i]["frame"] >= len(explosion):
                # Eliminamos la bomba si llega al último sprite
                bomb_positions[i] = None
                continue
                
            current_frame = int(bomb_states[i]["frame"])
            if current_frame < len(explosion):
                scaled_explosion = pygame.transform.scale(
                    explosion[current_frame],
                    (int(explosion[current_frame].get_width() * BOMB_SCALE),
                    int(explosion[current_frame].get_height() * BOMB_SCALE))
                )
                PANTALLA.blit(scaled_explosion,
                            (bomb["x"] - camera_x - scaled_explosion.get_width()//2,
                            bomb["y"] - camera_y - scaled_explosion.get_height()//2))
        else:
            PANTALLA.blit(scaled_bomb,
                        (bomb["x"] - camera_x - scaled_bomb.get_width()//2,
                        bomb["y"] - camera_y - scaled_bomb.get_height()//2))
    # Dibujar enemigos
    for enemy in enemy_positions:
        PANTALLA.blit(enemy["sprite"], 
                     (enemy["x"] - camera_x - enemy["sprite"].get_width()//2,
                      enemy["y"] - camera_y - enemy["sprite"].get_height()//2))
    
    # Filtrar las bombas que no son None antes de dibujarlas
    bomb_positions = [bomb for bomb in bomb_positions if bomb is not None]

    # Dibujar bombas
    for bomb in bomb_positions:
        if bomb:
            PANTALLA.blit(scaled_bomb,
                        (bomb["x"] - camera_x - scaled_bomb.get_width()//2,
                        bomb["y"] - camera_y - scaled_bomb.get_height()//2))
    
    # Si se ejecutó el path finding se dibuja la línea:
    if current_path and show_path:
        draw_path(PANTALLA, current_path, camera_x, camera_y)
    
    pygame.display.flip()

# FIN BUCLE DE JUEGO #

