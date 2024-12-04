from DynamicSeek import DynamicSeek
from SteeringOutput import SteeringOutput
from Vector import Vector
from Path import Path
from Kinematic import Kinematic

class FollowPath(DynamicSeek):
    def __init__(self, character: Kinematic, path: Path, max_acceleration: float, path_offset: float, predict_time: float, max_distance: float, screen_width: int, screen_height: int):
        super().__init__(character, Kinematic(Vector(0, 0), 0, Vector(0, 0), 0), max_acceleration, max_distance, screen_width, screen_height)
        self.path = path
        self.path_offset = path_offset
        self.predict_time = predict_time
        self.current_param = 0

    def getSteering(self) -> SteeringOutput:
        # Calcular la posición futura
        future_pos = self.character.position + self.character.velocity * self.predict_time

        # Obtener el parámetro actual en el camino
        self.current_param = self.path.getParam(future_pos, self.current_param)

        # Calcular el parámetro objetivo
        target_param = self.current_param + self.path_offset

        # Obtener la posición objetivo en el camino
        self.target.position = self.path.getPosition(target_param)

        # Usar el comportamiento de búsqueda para obtener el steering
        return super().getSteering()