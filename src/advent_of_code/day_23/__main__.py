from typing import List, Set

from advent_of_code.shared import (
    EdgeBidirectional,
    Graph,
    Node,
    PriorityList,
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

    # def find_clusters(self) -> List[Set[EdgeBidirectional]]:
    #     """Find all the groups of commonly connected nodes in the graph"""
    #
    #     clusters = []
    #
    #     # Go over all nodes and see how big their network is:
    #     for main_node in self.graph.nodes:
    #
    #
    #     return clusters

    # def grow_cluster(self,  starting_node: Node) -> Set[EdgeBidirectional]:
    #     """Recursively add to a cluster."""
    #
    #     cluster_nodes = set()
    #     cluster_edges = set()
    #
    #     # Keep a list of the latest nodes that we add, so we can grow from only those:
    #     outer_nodes = [starting_node]
    #     while outer_nodes:
    #         new_node = outer_nodes.pop(0)
    #         cluster_nodes.add(new_node)
    #
    #         # All potential edges also part of this cluster:
    #         for edge in self.graph.edges_by_node(new_node):
    #             connected_with_all = all(
    #                 cluster_node in edge.nodes
    #                 for cluster_node in cluster
    #             )  # `True` if

    def find_largest_cluster(self):

        # Defined clusters, prioritized by their size:
        clusters_queue = PriorityList[Set[Node]]()

        # Add the entire graph as we have it:
        for node in self.graph.nodes:
            clusters_queue.push(1, {node})

        biggest_cluster: Set[Node] = set()

        while clusters_queue:
            _, cluster = clusters_queue.pop()
            # For each node in the cluster, check if there are new fully connected
            # nodes:
            # for cluster_node in cluster:
            #     for potential_edge in self.graph.edges_by_node[cluster_node]:
            #         potential_node = potential_edge.get_other_node(
            #             cluster_node, check_first=False
            #         )
            #
            #         for checking_node in cluster:
            #             if checking_node == cluster_node:
            #                 continue

            new_nodes: None | Set[Node] = None
            for cluster_node in cluster:
                connected_nodes = {
                    n for _, n in self.graph.get_connected_nodes(cluster_node)
                }
                if new_nodes is None:
                    new_nodes = connected_nodes
                else:
                    new_nodes = new_nodes.intersection(connected_nodes)

            if not new_nodes:
                # No new connected nodes, this cluster is finished
                if len(cluster) > len(biggest_cluster):
                    biggest_cluster = cluster
            else:
                for new_node in new_nodes:
                    new_cluster = cluster | {new_node}
                    clusters_queue.push(len(new_cluster), new_cluster)

        return biggest_cluster


if __name__ == "__main__":
    main(Day23)
