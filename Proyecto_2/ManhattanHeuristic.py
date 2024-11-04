from A import Heuristic
from Nodo import TileNode
from Nodo import Node

class ManhattanHeuristic(Heuristic):
    def estimate_between(self, from_node: Node, to_node: Node) -> float:
        from_tile = from_node
        to_tile = to_node
        if isinstance(from_node, TileNode) and isinstance(to_node, TileNode):
            return abs(from_tile.x - to_tile.x) + abs(from_tile.y - to_tile.y)
        return 0