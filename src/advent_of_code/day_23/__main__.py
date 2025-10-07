from typing import Set

from advent_of_code.shared import EdgeBidirectional, Graph, Solver, main


class Day23(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.graph = Graph()

    def __call__(self) -> str:
        for line in self.iterate_input():
            node_1, _, node_2 = line.strip().partition("-")
            self.graph.add_edge_and_nodes(EdgeBidirectional, node_1, node_2)

        triangles = self.find_triangles()

        # Count how many of those triangles contain a node starting with "t":
        result = 0
        for triangle in triangles:
            found = False
            for edge in triangle:
                if any(node.name.startswith("t") for node in edge.nodes):
                    found = True
                    break

            if found:
                result += 1

        return str(result)

    def find_triangles(self) -> Set[Set[EdgeBidirectional]]:
        """Find connected triangles in the graph."""
        groups = set()
        # ^ collection of interconnected groups

        # Look over all edges in the graph:
        for main_edge in self.graph.edges:
            # Now cross-check all the other edges of these two connected nodes:
            node_1, node_2 = main_edge.nodes
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


if __name__ == "__main__":
    main(Day23)
