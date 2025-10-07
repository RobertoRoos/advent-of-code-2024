from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple, Type


@dataclass
class Node:
    """A point in a graph."""

    name: str

    def __hash__(self):
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Node({self.name})"


class EdgeBase(ABC):
    """Abstract edge base class."""

    nodes: Iterable[Node]
    cost: None | int | float

    def __init__(self, node_1: Node, node_2: Node, cost=None):
        self.cost = cost

    def __repr__(self) -> str:
        txt = ",".join(node.name for node in self.nodes)
        return f"Edge({txt}, cost={self.cost})"


class Edge(EdgeBase):
    """A one-directional edge from a graph.

    It connects one node towards another node.
    """

    def __init__(self, node_1: Node, node_2: Node, cost=None):
        self.nodes: Tuple[Node, Node] = tuple([node_1, node_2])
        super().__init__(node_1, node_2, cost=cost)


class EdgeBidirectional(EdgeBase):
    """A bidirectional edge.

    Connects two nodes without a preferred direction.
    """

    def __init__(self, node_1: Node, node_2: Node, cost=None):
        self.nodes: Set[Node] = {node_1, node_2}
        super().__init__(node_1, node_2, cost=cost)


class Graph:
    """A collection of edges and nodes."""

    def __init__(self):
        self.edges: Set[EdgeBase] = set()
        self.nodes: Set[Node] = set()

        self.edges_by_node: Dict[Node, List[EdgeBase]] = defaultdict(list)

    def add_edge(self, edge: EdgeBase):
        # Update sets:
        length_before = len(self.edges)
        self.edges.add(edge)

        if len(self.edges) == length_before:
            return  # A bit silly, but this prevents duplicate-ness checks twice

        # Also update helper look-ups:
        self.nodes |= edge.nodes
        for node in edge.nodes:
            self.edges_by_node[node].append(edge)

    def add_and_create_edge(
        self, edge_type: Type, node_1: Node, node_2: Node, cost=None
    ):
        new_edge: EdgeBase = edge_type(node_1, node_2, cost=cost)
        self.add_edge(new_edge)

    def add_edge_and_nodes(self, edge_type: Type, node_1: str, node_2: str, cost=None):
        self.add_and_create_edge(
            edge_type=edge_type, node_1=Node(node_1), node_2=Node(node_2), cost=cost
        )
