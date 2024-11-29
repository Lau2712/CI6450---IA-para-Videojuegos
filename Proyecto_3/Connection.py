from Nodo import Node

class Connection:
    def __init__(self, from_node: Node, to_node: Node, cost: float):
        self.from_node = from_node
        self.to_node = to_node
        self._cost = cost

    def get_cost(self) -> float:
        return self._cost
    
    def getFromNode(self) -> Node:
        return self.from_node
    
    def getToNode(self) -> Node:
        return self.to_node
