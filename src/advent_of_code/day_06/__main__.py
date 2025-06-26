from advent_of_code.shared import Direction, Grid, Solver, main


class Day06(Solver):

    def __call__(self) -> str:

        grid = Grid()

        for line in self.iterate_input():
            grid.add_str_row(line)

        guard = grid.get_item_by_character("^")
        grid.remove(guard)
        guard.direction = Direction.NORTH

        # Walk guard through the grid:
        number_steps = 0
        while grid.in_range(guard.coord):

            # Find next coordinate:
            turns = 0
            next_coord = None
            while turns < 4:
                next_coord = guard.coord.next(guard.direction)
                if next_coord not in grid.items:
                    break  # Empty tile

                # Blocked, so rotate
                guard.direction = guard.direction.rotate()
                turns += 1

            if next_coord is None:
                raise ValueError("Failed to find a next tile")

            guard.coord = next_coord
            number_steps += 1

        return ""


if __name__ == "__main__":
    main(Day06)
