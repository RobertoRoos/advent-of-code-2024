from collections import defaultdict
from typing import DefaultDict, FrozenSet, Set

from advent_of_code.shared import (
    EdgeBidirectional,
    Graph,
    Node,
    Solver,
    main,
)


class Day23(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.graph = Graph()

    def __call__(self) -> str:
        for line in self.iterate_input():
            node_1, _, node_2 = line.strip().partition("-")
            self.graph.add_edge_and_nodes(EdgeBidirectional, node_1, node_2)

        if self.args.part == 1:

            triangles = self.find_triangles()

            # Count how many of those triangles contain an edge, containing a node
            # starting with "t":
            result = 0
            for triangle in triangles:
                if any(
                    any(node.name.startswith("t") for node in edge.nodes)
                    for edge in triangle
                ):
                    result += 1

            return str(result)

        else:

            cluster = self.find_largest_cluster()

            node_names = [node.name for node in cluster]
            node_names = sorted(node_names)

            return ",".join(node_names)

    def find_triangles(self) -> Set[Set[EdgeBidirectional]]:
        """Find connected triangles in the graph."""
        groups = set()
        # ^ collection of interconnected groups

        # Look over all edges in the graph:
        for main_edge in self.graph.edges:
            # Now cross-check all the other edges of these two connected nodes:
            node_1, node_2 = main_edge.nodes

            edge_node_1: EdgeBidirectional
            for edge_node_1 in self.graph.edges_by_node[node_1]:
                if edge_node_1 == main_edge:
                    continue

                for edge_node_2 in self.graph.edges_by_node[node_2]:
                    if edge_node_2 == main_edge:
                        continue

                    # If these other two edges share a node, the three edges
                    # must make a triangle:
                    if not edge_node_1.nodes.isdisjoint(edge_node_2.nodes):
                        groups.add(frozenset([main_edge, edge_node_1, edge_node_2]))

        return groups

    def find_largest_cluster(self):
        """Find the largest cluster in the graph.

        We call a cluster a group of nodes that are all interconnected.

        We do this by keeping a queue of clusters-in-progress. For every item here
        we look for new nodes that are connected to all cluster members and add it
        to a new cluster, which is appended to the queue. While we work we can track
        the largest clusters we've encountered.
        This leads to many parallel clusters, but I think this is necessary as
        purposefully leaving out a potential extra node can always lead to more nodes
        in the future.
        """

        # Build a quick look-up of which nodes connects to which:
        all_connected_nodes: DefaultDict[Node, FrozenSet[Node]] = defaultdict(frozenset)
        for node in self.graph.nodes:
            all_connected_nodes[node] = frozenset(
                n for _, n in self.graph.get_connected_nodes(node)
            )

        # Defined clusters:
        clusters_queue: Set[FrozenSet[Node]] = set()
        # We keep the queue as a set itself, instead of a list, to prevent handling
        # duplicate clusters in the work queue.

        # Add the entire graph as we have it, each edge as a cluster:
        for edge in self.graph.edges:
            clusters_queue.add(frozenset(edge.nodes))

        biggest_cluster: FrozenSet[Node] = frozenset()

        while clusters_queue:
            cluster = clusters_queue.pop()

            # Keep a continually adjusting set of nodes that are connected to all
            # nodes in the current cluster
            new_nodes: None | Set[Node] = None
            for node in cluster:
                connected_nodes = all_connected_nodes[node]

                if new_nodes is None:
                    new_nodes = set(connected_nodes)
                else:
                    new_nodes.intersection_update(connected_nodes)

                if not new_nodes:
                    break

            if not new_nodes:
                # No new connected nodes, this cluster is finished
                if len(cluster) > len(biggest_cluster):
                    biggest_cluster = cluster
            else:
                for new_node in new_nodes:
                    new_cluster = frozenset(cluster | {new_node})
                    clusters_queue.add(new_cluster)

        return biggest_cluster


if __name__ == "__main__":
    main(Day23)
