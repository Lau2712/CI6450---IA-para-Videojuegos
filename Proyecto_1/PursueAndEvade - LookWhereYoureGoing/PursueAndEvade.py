from DynamicSeek import DynamicSeek
from Kinematic import Kinematic
from SteeringOutput import SteeringOutput

class Pursue(DynamicSeek):
    
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, max_distance: float, screen_width: int, screen_height: int, max_prediction: float, evade: bool):
        super().__init__(character, target, max_acceleration, max_distance, screen_width, screen_height)
        self.max_prediction = max_prediction
        self.evade = evade
    
    def getSteering(self) -> SteeringOutput:
        # Calculamos la dirección al objetivo
        direction = self.target.position - self.character.position
        distance = direction.magnitude()

        # Calculamos la velocidad actual
        speed = self.character.velocity.magnitude()
        
        # Calculamos el tiempo de predicción
        prediction = 0
        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction
        else:
            prediction = distance / speed
            
        # Calculamos la posición futura
        futurePosition = self.target.position + self.target.velocity * prediction

        # Intercambiamos momentaneamente las posiciones
        actual_target_position = self.target.position
        self.target.position = futurePosition
        
        # Usamos DynamicSeek para obtener el steering
        result = super().getSteering()

        # Restauramos la posición actual
        self.target.position = actual_target_position

        # Si deseamos evadir, invertimos la velocidad
        if self.evade:
            result.linear = result.linear * -1

        return result
