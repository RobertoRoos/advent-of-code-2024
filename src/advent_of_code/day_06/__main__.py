from typing import Set

from advent_of_code.shared import Direction, Grid, RowCol, Solver, main


class Day06(Solver):

    def __call__(self) -> str:

        grid = Grid()

        for line in self.iterate_input():
            grid.add_str_row(line)

        guard = grid.get_item_by_character("^")
        grid.remove(guard)
        guard.direction = Direction.NORTH

        # Walk guard through the grid:
        locations_visited: Set[RowCol] = set()
        while grid.in_range(guard.loc):

            locations_visited.add(guard.loc.copy())

            # Find next location:
            turns = 0
            from_direction = guard.direction.opposite()
            next_loc = None
            while turns < 3:
                next_loc = guard.loc.next(guard.direction)
                if next_loc not in grid.items:
                    break  # Empty tile

                # Blocked, so rotate
                guard.direction = guard.direction.rotate()
                if guard.direction == from_direction:
                    guard.direction = guard.direction.rotate()
                turns += 1

            if next_loc is None:
                raise ValueError("Failed to find a next tile")

            guard.loc = next_loc

        return str(len(locations_visited))


if __name__ == "__main__":
    main(Day06)
