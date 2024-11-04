from typing import List, Optional
from dataclasses import dataclass
from Grafo import Graph
from Nodo import Node
from Connection import Connection

@dataclass
class NodeRecord:
    node: Node
    connection: Optional[Connection] = None
    cost_so_far: float = float('inf')

class PathfindingList:
    def __init__(self):
        self.records: List[NodeRecord] = []
    
    def __len__(self):
        return len(self.records)
    
    def add(self, record: NodeRecord):
        self.records.append(record)
    
    def remove(self, record: NodeRecord):
        self.records.remove(record)
    
    def contains(self, node: Node) -> bool:
        return any(record.node == node for record in self.records)
    
    def find(self, node: Node) -> Optional[NodeRecord]:
        for record in self.records:
            if record.node == node:
                return record
        return None
    
    def smallest_element(self) -> NodeRecord:
        return min(self.records, key=lambda x: x.cost_so_far)

def pathfind_dijkstra(graph: Graph, start: Node, goal: Node) -> Optional[List[Connection]]:
    # Initialize the record for the start node
    start_record = NodeRecord(node=start, cost_so_far=0)
    
    # Initialize the open and closed lists
    open_list = PathfindingList()
    open_list.add(start_record)
    closed_list = PathfindingList()
    
    # Iterate through processing each node
    while len(open_list) > 0:
        current = open_list.smallest_element()
        
        # If it is the goal node, then terminate
        if current.node == goal:
            break
            
        # Get its outgoing connections
        connections = graph.get_connections(current.node)
        
        # Loop through each connection
        for connection in connections:
            end_node = connection.to_node
            end_node_cost = current.cost_so_far + connection.get_cost()
            
            # Skip if the node is closed
            if closed_list.contains(end_node):
                continue
                
            # Check if node is open
            elif open_list.contains(end_node):
                end_node_record = open_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
            else:
                end_node_record = NodeRecord(node=end_node)
                
            # Update the node record
            end_node_record.cost_so_far = end_node_cost
            end_node_record.connection = connection
            
            # Add it to open list if not already there
            if not open_list.contains(end_node):
                open_list.add(end_node_record)
                
        # Move current node from open to closed
        open_list.remove(current)
        closed_list.add(current)
    
    # Return null if no path found
    if current.node != goal:
        return None
        
    # Compile the path
    path = []
    
    # Work back along the path
    while current.node != start:
        path.append(current.connection)
        current = closed_list.find(current.connection.from_node)
        
    # Reverse the path and return it
    path.reverse()
    return path