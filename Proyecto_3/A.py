from typing import List, Optional
from dataclasses import dataclass
from Grafo import Graph
from Nodo import Node
from Connection import Connection
from abc import ABC, abstractmethod

class Heuristic(ABC):
    def __init__(self, goal_node: Node):
        self.goal_node = goal_node
    
    def estimate(self, from_node: Node) -> float:
        return self.estimate_between(from_node, self.goal_node)
    
    @abstractmethod
    def estimate_between(self, from_node: Node, to_node: Node) -> float:
        dx = abs(to_node.x - from_node.x)
        dy = abs(to_node.y - from_node.y)
        return dx + dy

@dataclass
class NodeRecord:
    node: Node
    connection: Optional[Connection] = None
    cost_so_far: float = float('inf')
    estimated_total_cost: float = float('inf')

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
        return min(self.records, key=lambda x: x.estimated_total_cost)

def pathfind_astar(graph: Graph, start: Node, goal: Node, heuristic: Heuristic) -> Optional[List[Connection]]:
    start_record = NodeRecord(
        node=start,
        cost_so_far=0,
        estimated_total_cost=heuristic.estimate(start)
    )
    
    open_list = PathfindingList()
    open_list.add(start_record)
    closed_list = PathfindingList()
    
    while len(open_list) > 0:
        current = open_list.smallest_element()

        if current.node == goal:
            break

        connections = graph.get_connections(current.node)

        for connection in connections:
            end_node = connection.to_node
            end_node_cost = current.cost_so_far + connection.get_cost()

            if closed_list.contains(end_node):
                end_node_record = closed_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
                closed_list.remove(end_node_record)
                end_node_heuristic = end_node_record.estimated_total_cost - end_node_record.cost_so_far

            elif open_list.contains(end_node):
                end_node_record = open_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
                end_node_heuristic = end_node_record.estimated_total_cost - end_node_record.cost_so_far

            else:
                end_node_record = NodeRecord(node=end_node)
                end_node_heuristic = heuristic.estimate(end_node)

            end_node_record.cost_so_far = end_node_cost
            end_node_record.connection = connection
            end_node_record.estimated_total_cost = end_node_cost + end_node_heuristic

            if not open_list.contains(end_node):
                open_list.add(end_node_record)

        open_list.remove(current)
        closed_list.add(current)

    if current.node != goal:
        return None

    path = []
    
    while current.node != start:
        path.append(current.connection)
        current = closed_list.find(current.connection.from_node)

    path.reverse()
    return path