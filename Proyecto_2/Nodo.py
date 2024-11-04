class Node:
    def __init__(self, name):
        self.name = name

class TileNode(Node):
    def __init__(self, x: int, y: int):
        super().__init__(f"tile_{x}_{y}")
        self.x = x
        self.y = y