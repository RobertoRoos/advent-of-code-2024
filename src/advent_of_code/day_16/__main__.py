from collections import defaultdict
from heapq import heappop, heappush
from typing import DefaultDict, Dict, List, Tuple

from advent_of_code.shared import Direction, Grid, GridItem, RowCol, Solver, main

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

    def find_new_direction(
        self, direction: Direction, options: Dict[Direction, int]
    ) -> int:
        """Return the cost of a new direction based on a list of options."""
        if direction in options:
            return options[direction]

        best_score = None

        for option_direction, option_score in options.items():
            new_score = option_score + self.COST_TURN * abs(
                option_direction.turns(direction, go_negative=True)
            )

            if best_score is None or new_score < best_score:
                best_score = new_score

        return best_score

    def get_lowest_score_queue(self, start: GridItem, end: GridItem) -> int:
        """Use Dijkstra's to find the best path."""
        random_counter = 0

        path_queue: List[Tuple[int, int, Path]] = [
            (0, random_counter, [(start.loc, start.direction)])
        ]
        # Entries are like: `(<score>, <random counter>, <path so far>)`
        # We add the random counter to ensure that sorting will not rely on location
        # or direction
        random_counter += 1

        best_scores: DefaultDict[RowCol, Dict[Direction, int]] = defaultdict(dict)
        # Track the lowest score to get to a point with a certain direction
        # Entries are like `{<loc>: {<direction>: <score>}}", with <score> the
        # sum of cost

        while len(path_queue) > 0:
            # Consume the lowest-score option from the queue:
            this_score, _, this_path = heappop(path_queue)

            tip_loc: RowCol
            tip_direction: Direction
            tip_loc, tip_direction = this_path[-1]  # Find where this path ends

            if tip_loc == end.loc:
                return best_scores[tip_loc][tip_direction]

            # Check 4 possible directions:
            for next_direction in Direction:
                if next_direction == tip_direction.opposite():
                    continue  # Don't bother doubling back

                next_loc = tip_loc.next(next_direction)
                next_tile = self.grid.items.get(next_loc, None)
                if next_tile is not None and next_tile.character == "#":
                    continue  # Cannot go this way, skip

                turns = 0 if next_direction == tip_direction else 1  # Never backwards
                next_score = this_score + self.COST_STEP + self.COST_TURN * turns

                if (
                    next_direction not in best_scores[next_loc]
                    or next_score < best_scores[next_loc][next_direction]
                ):
                    # Found a better path!
                    next_path = this_path[:] + [(next_loc, next_direction)]
                    best_scores[next_loc][next_direction] = next_score
                    heappush(
                        path_queue,
                        (next_score, random_counter, next_path),
                    )
                    random_counter += 1

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

        self.grid.print()
        print()
        print_grid.print()
        print()
        # print_grid.print(data_key="score", padding=8)
        # print()


if __name__ == "__main__":
    main(Day16)
