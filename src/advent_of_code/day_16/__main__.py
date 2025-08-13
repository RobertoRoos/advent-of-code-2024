from collections import defaultdict
from typing import Dict

from advent_of_code.shared import Direction, Grid, GridItem, RowCol, Solver, main


class Day16(Solver):

    COST_STEP = 1
    COST_TURN = 1_000

    def __call__(self) -> str:

        grid = Grid()

        for line in self.iterate_input():
            grid.add_str_row(line)

        start = grid.get_item_by_character("S")
        start.direction = Direction.EAST
        end = grid.get_item_by_character("E")

        score = self.get_lowest_score(grid, start, end)

        return str(score)

    def get_lowest_score(self, grid: Grid, start: GridItem, end: GridItem) -> int:
        """Solve the problem of finding a lowest score.

        We solve this by 'flooding' the maze from the start: for each neighbouring tile
        we check what the potential cost would be to get there. When a cost for this
        tile was already present but the new is lower, we replaced the stored one. Once
        every tile has run out, we check the number on the exit tile.
        Since orientation matters, we need to track not just every tile but also every
        position in every tile.
        """
        tile_scores: Dict[RowCol, Dict[Direction, int]] = defaultdict(dict)
        # Like: { coord: { direction: lowest score } }

        tile_scores[start.loc][start.direction] = 0

        still_changing = True
        while still_changing:
            still_changing = False

            # Loop over every tile that we already have a score for
            for loc in list(tile_scores):
                direction_scores = tile_scores[loc]
                # Loop over copy of dict keys to allow resizing

                if len(direction_scores) < 4:
                    for direction in Direction:
                        if direction not in direction_scores:
                            new_score = self.find_new_direction(
                                direction, direction_scores
                            )
                            direction_scores[direction] = new_score

                # Loop over neighbouring tiles for this location
                for next_direction in Direction:
                    neighbour_loc = loc.next(next_direction)
                    neighbour = grid.items.get(neighbour_loc, None)
                    if neighbour is not None and neighbour.character == "#":
                        continue  # Wall - cannot do anything here

                    new_score = direction_scores[next_direction] + self.COST_STEP
                    if (
                        next_direction not in tile_scores[neighbour_loc]
                        or new_score < tile_scores[neighbour_loc][next_direction]
                    ):
                        tile_scores[neighbour_loc][next_direction] = new_score
                        still_changing = True

        scores_end = tile_scores[end.loc]

        return min(scores_end.values())

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


if __name__ == "__main__":
    main(Day16)
