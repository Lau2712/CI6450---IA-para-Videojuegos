from Decision_Tree import Action, Decision
from Kinematic import Kinematic
from Vector import Vector
from DynamicFlee import DynamicFlee
import math

class DynamicFleeAction(Action):
    def __init__(self, enemy, player, max_acceleration, max_distance, screen_width, screen_height, min_x, max_x):
        self.enemy = enemy
        self.player = player
        self.max_acceleration = max_acceleration
        self.max_distance = max_distance
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.min_x = min_x
        self.max_x = max_x
    
    def getSteering(self):
        enemy_kinematic = Kinematic(Vector(self.enemy["x"], self.enemy["y"]), 0, Vector(0,0), 0)
        player_kinematic = Kinematic(Vector(self.player[0], self.player[1]), 0, Vector(0,0), 0)
        
        flee_behavior = DynamicFlee(
            enemy_kinematic,
            player_kinematic,
            self.max_acceleration,
            self.max_distance,
            self.screen_width,
            self.screen_height
        )
        
        return flee_behavior.getSteering()
        
    def make_decision(self):
        enemy_kinematic = Kinematic(Vector(self.enemy["x"], self.enemy["y"]), 0, Vector(0,0), 0)
        player_kinematic = Kinematic(Vector(self.player[0], self.player[1]), 0, Vector(0,0), 0)
        
        dx = self.enemy["x"] - self.player[0]
        dy = self.enemy["y"] - self.player[1]
        distance = (dx*dx + dy*dy)**0.5
        
        if distance <= self.max_distance:
            flee_behavior = DynamicFlee(
                enemy_kinematic,
                player_kinematic,
                self.max_acceleration,
                self.max_distance,
                self.screen_width,
                self.screen_height
            )
        
            steering = flee_behavior.getSteering()
            if steering:
                new_x = self.enemy["x"] + steering.linear.x
                # Limitamos el movimiento horizontal
                if self.min_x <= new_x <= self.max_x:
                    self.enemy["x"] = new_x
                    self.enemy["y"] = enemy_kinematic.position.z
                    
            return flee_behavior
        return None

class DynamicFleeDecision(Decision):
    def __init__(self, enemy, player_pos, player_attacking, detection_radius, attack_action, patrol_action, min_x, max_x):
        super().__init__(attack_action, patrol_action)
        self.enemy = enemy
        self.player_pos = player_pos
        self.player_attacking = player_attacking
        self.detection_radius = detection_radius
        #self.dynamic_flee = dynamic_flee
        self.min_x = min_x
        self.max_x = max_x

    def test_value(self):
        # Calcula la distancia al jugador
        dx = self.player_pos[0] - self.enemy["x"]
        dy = self.player_pos[1] - self.enemy["y"]
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Verifica si está en rango
        return distance <= self.detection_radius
        
    def make_decision(self):
        if self.test_value():
            if self.player_attacking:
                #return self.dynamic_flee
                return "attack"
        return "patrol"