from collections import defaultdict
from heapq import heappop, heappush
from typing import Dict, List, Tuple, Set

from advent_of_code.shared import Direction, Grid, GridItem, RowCol, Solver, main


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
        tiles_queue: List[Tuple[int, int, RowCol, Direction]] = []
        # Entries are like `(<score>, <random counter>, <loc>, <direction>)`
        # We add the random counter to ensure that sorting will not rely on location
        # or direction
        scores = defaultdict(dict)
        # Entries are like `{<loc>: {<direction>: <score>}}", with <score> the
        # sum of cost
        prev = defaultdict(dict)
        # Entries are like "{<loc>: {<dir>: (<loc_prev>, <dir_prev>)}"

        random_counter = 0

        heappush(tiles_queue, (0, random_counter, start.loc, start.direction))
        random_counter += 1
        scores[start.loc][start.direction] = 0
        best_score = None
        all_path_tiles: Set[RowCol] = set()  # All locations touched in any optimal path

        while tiles_queue:
            tip_score, _, tip_loc, tip_direction = heappop(tiles_queue)

            # Check all 4 neighbouring tiles:
            for next_direction in Direction:
                next_loc = tip_loc.next(next_direction)
                next_tile = self.grid.items.get(next_loc, None)
                if next_tile is not None and next_tile.character == "#":
                    continue  # Cannot go this way, skip

                turns = abs(tip_direction.turns(next_direction, go_negative=True))
                next_score = tip_score + self.COST_STEP + self.COST_TURN * turns

                if (
                    next_direction not in scores[next_loc]
                    or next_score < scores[next_loc][next_direction]
                ):
                    # Found a better path!
                    scores[next_loc][next_direction] = next_score
                    prev[next_loc][next_direction] = (tip_loc, tip_direction)
                    heappush(
                        tiles_queue,
                        (next_score, random_counter, next_loc, next_direction),
                    )
                    random_counter += 1

                    if best_score is None and next_loc == end.loc:
                        best_score = next_score

                if best_score is not None and next_loc == end.loc and next_score == best_score:
                    # This path is (also) a good one!
                    for step in self.parse_path(scores, prev, end):
                        all_path_tiles.add(step[0])

                    self.debug_print_route(scores, prev, end)

                    pass

        # self.debug_print_route(scores, prev, end)

        if self.args.part == 1:
            return min(scores[end.loc].values())
        else:
            return len(all_path_tiles)

    @staticmethod
    def parse_path(scores, prev, end: GridItem) -> List[Tuple[RowCol, Direction]]:
        """Takes the Dijkstra `prev` list and resolve to a list of locations."""
        end_scores = scores[end.loc]
        end_direction = min(end_scores, key=end_scores.get)
        # ^ Direction on the 'end' tile
        this_step = prev[end.loc][end_direction]

        steps: List[Tuple[RowCol, Direction]] = []

        while this_step is not None:
            try:
                this_step = prev[this_step[0]][this_step[1]]
            except KeyError:
                this_step = None
            else:
                steps.insert(0, this_step)

        return steps

    def debug_print_route(self, scores, prev, end: GridItem):
        """Visually print the solved path."""
        print_grid = Grid()
        print_grid.rows = self.grid.rows
        print_grid.cols = self.grid.cols

        for this_step in self.parse_path(scores, prev, end):
            this_step_tile = GridItem(character="+", loc=this_step[0])
            this_step_tile.data["score"] = scores[this_step[0]][this_step[1]]
            print_grid.add(this_step_tile)

        self.grid.print()
        print()
        print_grid.print()
        print()
        print_grid.print(data_key="score", padding=8)
        print()


if __name__ == "__main__":
    main(Day16)
