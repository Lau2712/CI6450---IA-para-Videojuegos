from Connection import Connection
from Nodo import Node
class Graph:
    def __init__(self):
        self.connections = {}

    def add_connection(self, from_node: Node, to_node: Node, cost: float):
        if from_node not in self.connections:
            self.connections[from_node] = []
        self.connections[from_node].append(Connection(from_node, to_node, cost))

    def get_connections(self, from_node: Node) -> list[Connection]:
        return self.connections.get(from_node, [])