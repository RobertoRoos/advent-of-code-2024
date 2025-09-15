from collections import defaultdict
from typing import DefaultDict, Dict, List, Set, Tuple

from advent_of_code.shared import (
    Direction,
    Grid,
    GridItem,
    PriorityList,
    RowCol,
    Solver,
    main,
)

Path = List[Tuple[RowCol, Direction]]


class Day16(Solver):

    COST_STEP = 1
    COST_TURN = 1_000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = Grid()

    def __call__(self) -> str:

        for line in self.iterate_input():
            self.grid.add_str_row(line)

        start = self.grid.get_item_by_character("S")
        start.direction = Direction.EAST
        end = self.grid.get_item_by_character("E")

        score = self.get_lowest_score_queue(start, end)

        return str(score)

    def get_lowest_score_queue(self, start: GridItem, end: GridItem) -> int:
        """Use Dijkstra's to find the best path."""
        path_queue = PriorityList[List[Tuple[RowCol, Direction]]]()
        path_queue.push(0, [(start.loc, start.direction)])
        # Entries are like: `[<path so far>]`

        best_scores: DefaultDict[RowCol, Dict[Direction, int]] = defaultdict(dict)
        # Track the lowest score to get to a point with a certain direction
        # Entries are like `{<loc>: {<direction>: <score>}}", with <score> the
        # sum of cost

        optimal_score: None | int = None
        # Track the score we would return

        all_path_tiles: Set[RowCol] = set()

        while path_queue:
            # Consume the lowest-score option from the queue:

            this_score, this_path = path_queue.pop()

            tip_loc, tip_direction = this_path[-1]  # Find where this path ends

            if tip_loc == end.loc:  # Found the (first of multiple) optimal path(s)

                if self.args.part == 1:
                    # Just return the score of the best path:
                    return this_score

                if optimal_score is None:
                    optimal_score = this_score

                if optimal_score is not None and this_score == optimal_score:
                    # Found a path that is the optimal path or just as good
                    all_path_tiles |= set(loc for loc, _ in this_path)

            # Check 4 possible directions:
            for next_direction in Direction:
                if next_direction == tip_direction.opposite():
                    continue  # Don't bother doubling back

                next_loc = tip_loc.next(next_direction)
                next_tile = self.grid.items.get(next_loc, None)
                if next_tile is not None and next_tile.character == "#":
                    continue  # Cannot go this way, skip

                if next_loc in [loc for loc, _ in this_path]:
                    continue  # We started making a loop, give up here
                # Not really needed in regular Dijkstra, but we use a lt-or-eq operator,
                # so this helps

                turns = 0 if next_direction == tip_direction else 1  # Never backwards
                next_score = this_score + self.COST_STEP + self.COST_TURN * turns

                if (
                    next_direction not in best_scores[next_loc]
                    or next_score < best_scores[next_loc][next_direction]
                    or (
                        self.args.part == 2
                        and next_score == best_scores[next_loc][next_direction]
                    )
                ):

                    # Found a better path!
                    next_path = this_path[:] + [(next_loc, next_direction)]
                    best_scores[next_loc][next_direction] = next_score
                    path_queue.push(next_score, next_path)

        if self.args.part == 2:
            return len(all_path_tiles)

        raise RuntimeError("Failed to find path")

    def debug_print_route(self, path: Path):
        """Visually print the solved path."""
        print_grid = Grid()
        print_grid.rows = self.grid.rows
        print_grid.cols = self.grid.cols

        for this_loc, _ in path:
            this_tile = GridItem(character="+", loc=this_loc)
            # this_tile.data["score"] = scores[this_step[0]][this_step[1]]
            print_grid.add(this_tile)

        # self.grid.print()
        # print()
        print_grid.print()
        print()
        # print_grid.print(data_key="score", padding=8)
        # print()


if __name__ == "__main__":
    main(Day16)
