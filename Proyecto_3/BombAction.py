from Decision_Tree import Action, Decision
import math

# Clase para definir la acción de atacar
class BombAttackAction(Action):
    def __init__(self, player, direction, attack_sprites_right, attack_sprites_left):
        self.player = player
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        return "attack"

# Clase para definir la acción de huir
class BombFleeAction(Action):
    def __init__(self, player, bombs, max_speed, max_distance, screen_width, screen_height):
        self.player = player
        self.bombs = bombs
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.screen_width = screen_width
        self.screen_height = screen_height


# Clase para definir la decisión de atacar o huir
class BombInteractionDecision(Decision):
    def __init__(self, player_pos, bombs, detection_radius, attack_action):
        super().__init__(attack_action, None)
        self.player_pos = player_pos
        self.bombs = bombs
        self.detection_radius = detection_radius
        
    def get_bombs_in_range(self):
        bombs_in_range = []
        for bomb in self.bombs:
            if bomb is not None:
                dx = self.player_pos[0] - bomb["x"]
                dy = self.player_pos[1] - bomb["y"]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance <= self.detection_radius:
                    bombs_in_range.append(bomb)
        return bombs_in_range
        
    def make_decision(self):
        bombs_in_range = self.get_bombs_in_range()
        
        if len(bombs_in_range) == 0:
            return None
        else:
            # Se ataca
            return "attack"
    
    def test_value(self):
        bombs_in_range = self.get_bombs_in_range()
        return len(bombs_in_range) == 1