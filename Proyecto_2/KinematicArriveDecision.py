from Decision_Tree import Action, Decision
from Static import static
from Vector import Vector
from KinematicArrive import KinematicArrive
import math

# Clase que representa la acción de Kinematic Arrive
class KinematicArriveAction(Action):
    def __init__(self, enemy, player, max_speed, arrival_radius):
        self.enemy = enemy
        self.player = player
        self.max_speed = max_speed
        self.arrival_radius = arrival_radius
        
    def make_decision(self):
        enemy_static = static(Vector(self.enemy["x"], self.enemy["y"]), 0)
        player_static = static(Vector(self.player[0], self.enemy["y"]), 0)
        return KinematicArrive(enemy_static, player_static, self.max_speed, self.arrival_radius)

# Clase que representa la acción de patrullar
class PatrolAction(Action):
    def __init__(self, enemy, direction):
        self.enemy = enemy
        self.direction = direction
        
    def make_decision(self):
        return "patrol"

# Clase que representa la decisión de patrullar o aplicar Kinematic Arrive
class InRangeDecision(Decision):
    def __init__(self, enemy_pos, player_pos, true_node, false_node, test_function):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.test_function = test_function
        
    def test_value(self):
        return self.test_function(self.enemy_pos, self.player_pos)

# Clase que representa la acción de atacar
class AttackAction(Action):
    def __init__(self, enemy, direction, attack_sprites_right, attack_sprites_left):
        self.enemy = enemy
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        return "attack"

# Clase que representa la decisión del jugador
class PlayerReachedDecision(Decision):
    def __init__(self, enemy_pos, player_pos, true_node, false_node, arrival_radius):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.arrival_radius = arrival_radius
        
    def test_value(self):
        dx = self.player_pos[0] - self.enemy_pos[0]
        dy = self.player_pos[1] - self.enemy_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        return isinstance(self.false_node.make_decision(), KinematicArrive) and distance <= self.arrival_radius

# Clase que representa la acción de desaparecer
class DisappearAction(Action):
    def __init__(self, enemy, direction, disappear_sprites_right, disappear_sprites_left):
        self.enemy = enemy
        self.direction = direction
        self.disappear_sprites_right = disappear_sprites_right
        self.disappear_sprites_left = disappear_sprites_left
        
    def make_decision(self):
        return "disappear"

# Clase que representa la decisión del jugador cuando está atacando
class PlayerAttackingInRangeDecision(Decision):
    def __init__(self, enemy_pos, player_pos, player_attacking, detection_radius, true_node, false_node):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.player_attacking = player_attacking
        self.detection_radius = detection_radius
        
    def test_value(self):
        dx = self.player_pos[0] - self.enemy_pos[0]
        dy = self.player_pos[1] - self.enemy_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)

        return self.player_attacking and distance <= self.detection_radius