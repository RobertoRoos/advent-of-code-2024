from collections import defaultdict
from typing import Dict, List, Set, Tuple

from advent_of_code.shared import Direction, Grid, GridItem, RowCol, Solver, main


class Day06(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = Grid()

    def __call__(self) -> str:

        for line in self.iterate_input():
            self.grid.add_str_row(line)

        guard = self.grid.get_item_by_character("^")
        self.grid.remove(guard)
        guard.direction = Direction.NORTH

        # Track which locations we passed and in which direction we entered them
        locations_visited: defaultdict[RowCol, Set[Direction]] = defaultdict(set)
        possible_blocks = 0  # Number of options to get the guard stuck in a loop

        # Walk guard through the grid:
        while self.grid.in_range(guard.loc):

            locations_visited[guard.loc.copy()].add(guard.direction)

            # Find next location:
            turns = 0
            from_direction = guard.direction.opposite()
            next_loc = None
            while turns < 3:
                next_loc = guard.loc.next(guard.direction)
                if next_loc not in self.grid.items:
                    break  # Empty tile

                # Blocked, so rotate
                guard.direction = guard.direction.rotate()
                if guard.direction == from_direction:
                    guard.direction = guard.direction.rotate()
                turns += 1

            if next_loc is None:
                raise ValueError("Failed to find a next tile")

            # Check for possible block:
            if self.args.part == 2:
                # What if we added a block at `next_loc`?
                if next_loc not in locations_visited:
                    # Don't interfere with the path so far
                    blocked_next_loc, blocked_next_direction = self.find_next_step(
                        guard, extra_block=next_loc
                    )
                    if blocked_next_direction in locations_visited[blocked_next_loc]:
                        possible_blocks += 1
                        print(next_loc)

            guard.loc = next_loc

        if self.args.part == 2:
            return str(possible_blocks)

        return str(len(locations_visited))

    def find_next_step(
        self, guard: GridItem, extra_block: RowCol | None = None
    ) -> Tuple[RowCol, Direction]:
        """Get the next tile the guard would move to, based on the grid.

        :return: Next tile and the direction to step into that tile
        """
        next_loc, next_direction = None, None
        for next_direction in guard.direction.next_options():
            next_loc = guard.loc.next(next_direction)
            if next_loc not in self.grid.items and (
                extra_block is None or extra_block != next_loc
            ):
                break  # Empty tile (also considering an extra block)

        if next_loc is None:
            raise ValueError("Failed to find a next tile")

        return next_loc, next_direction


if __name__ == "__main__":
    main(Day06)
