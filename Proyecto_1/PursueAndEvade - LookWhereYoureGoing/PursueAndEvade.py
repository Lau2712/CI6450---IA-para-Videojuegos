from DynamicSeek import DynamicSeek
from Kinematic import Kinematic
from SteeringOutput import SteeringOutput

class Pursue(DynamicSeek):
    
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, max_distance: float, screen_width: int, screen_height: int, max_prediction: float, evade: bool):
        super().__init__(character, target, max_acceleration, max_distance, screen_width, screen_height)
        self.max_prediction = max_prediction
        self.evade = evade
    
    def getSteering(self) -> SteeringOutput:
        # Calcular la dirección al objetivo
        direction = self.target.position - self.character.position
        distance = direction.magnitude()

        # Calcular la velocidad actual
        speed = self.character.velocity.magnitude()
        
        # Calcular el tiempo de predicción
        prediction = 0
        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction
        else:
            prediction = distance / speed
            
        # Calcular la posición futura del objetivo
        futurePosition = self.target.position + self.target.velocity * prediction

        # Temporalmente cambiar la posición del objetivo a la posición futura
        actual_target_position = self.target.position
        self.target.position = futurePosition
        
        # Obtener el steering utilizando el método de la clase padre (DynamicSeek)
        result = super().getSteering()

        # Restaurar la posición original del objetivo
        self.target.position = actual_target_position

        # Invertir la dirección si es evasión
        if self.evade:
            result.linear = result.linear * -1

        return result