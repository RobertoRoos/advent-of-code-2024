from collections import defaultdict
from typing import List, Set

from advent_of_code.shared import Grid, GridItem, RowCol, Solver, main


class Day10(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = Grid()

    def __call__(self) -> str:
        for line in self.iterate_input():
            self.grid.add_str_row(line)

        items_by_value: defaultdict[int, List[GridItem]] = defaultdict(list)

        # Fill in some meta-data:
        for item in self.grid.items.values():
            val = int(item.character)
            item.data["value"] = val
            items_by_value[val].append(item)

            item.data["ends"]: Set[RowCol] = set()  # Set of 9s that can be reached
            if val == 9:
                item.data["ends"].add(item.loc)

        # Go backwards from 9 to 0, keeping count of the tiles you can reach from there
        for value in range(9, -1, -1):
            for item in items_by_value[value]:
                # Check the neighbouring tiles:
                for neighbour in self.grid.neighbours(item):
                    if neighbour.data["value"] == value - 1:
                        neighbour.data["ends"] = neighbour.data["ends"].union(
                            item.data["ends"]
                        )

        scores_total = 0

        for item in items_by_value[0]:
            this_score = len(item.data["ends"])
            scores_total += this_score

        return str(scores_total)


if __name__ == "__main__":
    main(Day10)
