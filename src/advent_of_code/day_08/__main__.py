from collections import defaultdict
from typing import List, Set

from advent_of_code.shared import Grid, GridItem, RowCol, Solver, main


class Day08(Solver):

    def __call__(self) -> str:

        grid = Grid()

        for line in self.iterate_input():
            grid.add_str_row(line)

        # Group by characters:
        signals: defaultdict[str, List[GridItem]] = defaultdict(list)
        for item in grid.items.values():
            signals[item.character].append(item)

        anti_nodes: Set[RowCol] = set()

        limits = (1, 1) if self.args.part == 1 else (0, grid.rows)

        for nodes in signals.values():
            # Combine all pairs of nodes:
            for i1, node_1 in enumerate(nodes):
                for node_2 in nodes[i1 + 1 :]:
                    step = node_2.loc - node_1.loc

                    for i in range(limits[0], limits[1] + 1):
                        new_anti_nodes = [
                            node_1.loc - step * i,
                            node_2.loc + step * i,
                        ]

                        still_good = False  # Still something in range of the grid

                        for new_anti_node in new_anti_nodes:
                            if grid.in_range(new_anti_node):
                                anti_nodes.add(new_anti_node)
                                still_good = True

                        if not still_good:
                            break

        return str(len(anti_nodes))


if __name__ == "__main__":
    main(Day08)
