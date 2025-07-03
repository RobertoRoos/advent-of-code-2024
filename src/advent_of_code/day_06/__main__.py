from collections import defaultdict
from typing import Set, Tuple

from advent_of_code.shared import Direction, Grid, GridItem, RowCol, Solver, main

Locations = defaultdict[RowCol, Set[Direction]]


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

        if self.args.part == 1:
            steps = self.get_number_of_steps(self.grid, guard)
            return str(len(steps))

        else:

            possible_blocks: int = 0

            locations_visited: Locations = defaultdict(set)
            # ^ locations history of the real guard in the real maze

            # Do the loop again, but step-by-step:
            while self.grid.in_range(guard.loc):

                # Find next location:
                next_loc, next_dir = self.find_next_step(self.grid, guard)

                # What if that spot was a block instead:
                if next_loc not in locations_visited and self.grid.in_range(next_loc):
                    maze_temp = self.grid.copy()
                    maze_temp.items[next_loc] = GridItem(loc=next_loc, character="O")

                    guard_temp = GridItem(
                        loc=guard.loc.copy(), character=guard.character
                    )
                    guard_temp.direction = guard.direction

                    try:
                        locations_visited_copy = defaultdict(set)
                        for loc, item in locations_visited.items():
                            locations_visited_copy[loc.copy()] = item.copy()

                        self.get_number_of_steps(
                            maze_temp, guard_temp, locations_visited_copy
                        )
                    except RuntimeError:
                        # Catch loops:
                        possible_blocks += 1

                locations_visited[guard.loc.copy()].add(guard.direction)
                guard.loc = next_loc
                guard.direction = next_dir

            return str(possible_blocks)

    @staticmethod
    def find_next_step(maze: Grid, guard: GridItem) -> Tuple[RowCol, Direction]:
        """Get the next tile the guard would move to, based on the grid.

        :return: Next tile and the direction to step into that tile
        """
        next_loc, next_direction = None, None
        for next_direction in guard.direction.next_options():
            next_loc = guard.loc.next(next_direction)
            if next_loc not in maze.items:
                break  # Empty tile (also considering an extra block)

        if next_loc is None:
            raise ValueError("Failed to find a next tile")

        return next_loc, next_direction

    def get_number_of_steps(
        self, maze: Grid, guard: GridItem, locations_visited: Locations | None = None
    ) -> Locations:
        """Return number of steps until the guard leaves this maze.

        :raises: RuntimeError when the guard gets stuck in a loop instead.
        """

        # Track which locations we passed and in which direction we entered them
        if locations_visited is None:
            locations_visited = defaultdict(set)

        # Walk guard through the grid:
        while maze.in_range(guard.loc):

            loc = guard.loc.copy()
            if guard.direction in locations_visited[loc]:
                # If we already visited here and entered from this way it's a loop:
                raise RuntimeError("Loop detected!")

            locations_visited[loc].add(guard.direction)

            # Find next location:
            guard.loc, guard.direction = self.find_next_step(maze, guard)

        return locations_visited


if __name__ == "__main__":
    main(Day06)
