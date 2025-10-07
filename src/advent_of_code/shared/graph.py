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

    def get_other_node(self, other_node: Node, check_first: bool = True) -> Node:
        """Given one node, return the other one of this edge."""

        if check_first:
            if other_node not in self.nodes:
                raise ValueError(f"Node {other_node} isn't in this edge to begin with")

        for node in self.nodes:
            if node != other_node:
                return node

        raise ValueError(f"Failed to get other node of {other_node}")


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

        self.edges_by_node: Dict[Node, Set[EdgeBase]] = defaultdict(set)

    def add_edge(self, edge: EdgeBase):
        # Update sets:
        length_before = len(self.edges)
        self.edges.add(edge)

        if len(self.edges) == length_before:
            return  # A bit silly, but this prevents duplicate-ness checks twice

        # Also update helper look-ups:
        self.nodes |= edge.nodes
        for node in edge.nodes:
            self.edges_by_node[node].add(edge)

    def add_and_create_edge(
        self, edge_type: Type, node_1: Node, node_2: Node, cost=None
    ):
        new_edge: EdgeBase = edge_type(node_1, node_2, cost=cost)
        self.add_edge(new_edge)

    def add_edge_and_nodes(self, edge_type: Type, node_1: str, node_2: str, cost=None):
        self.add_and_create_edge(
            edge_type=edge_type, node_1=Node(node_1), node_2=Node(node_2), cost=cost
        )

    def get_connected_nodes(self, node: Node) -> Set[Tuple[EdgeBase, Node]]:
        """Return a set of other nodes (and their edge) the given nodes connects to."""
        return {
            (edge, edge.get_other_node(node, check_first=False))
            for edge in self.edges_by_node[node]
        }

    def get_edge(self, node_1: Node, node_2: Node) -> EdgeBase | None:
        """Get the edge between two nodes, or ``None``."""

        overlapping_edges = self.edges_by_node[node_1].intersection(
            self.edges_by_node[node_2]
        )

        if not overlapping_edges:
            return None
        else:
            return next(iter(overlapping_edges))
