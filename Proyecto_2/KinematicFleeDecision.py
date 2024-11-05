from Decision_Tree import Action
from Static import static
from Vector import Vector
from KinematicFlee import KinematicFlee

class KinematicFleeAction(Action):
    def __init__(self, enemy, player, max_speed, max_distance, screen_width, screen_height):
        self.enemy = enemy
        self.player = player
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def make_decision(self):
        enemy_static = static(Vector(self.enemy["x"], self.enemy["y"]), 0)
        player_static = static(Vector(self.player[0], self.player[1]), 0)
        
        return KinematicFlee(
            enemy_static, 
            player_static, 
            self.max_speed,
            self.max_distance,
            self.screen_width,
            self.screen_height
        )