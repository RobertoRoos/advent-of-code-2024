from typing import List

from advent_of_code.shared import Direction, Grid, RowCol, Solver, main


class Day20(Solver):

    CHEAT_MINIMUM: int = 100  # Minimum numer of picoseconds to save (inclusive)
    CHEAT_DURATION: int = 20  # Number of steps to take while cheating (part 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = Grid()

    def __call__(self) -> str:
        for line in self.iterate_input():
            self.grid.add_str_row(line)

        start = self.grid.get_item_by_character("S")
        goal = self.grid.get_item_by_character("E")

        maze_path = self.solve_maze(start.loc, goal.loc)

        duration = 2 if self.args.part == 1 else self.CHEAT_DURATION
        cheats = self.find_any_cheats(maze_path, duration, self.CHEAT_MINIMUM)

        return str(cheats)

    def solve_maze(self, start: RowCol, goal: RowCol) -> List[RowCol]:
        """Trace the maze solution.

        Assumes only a single solution exists!
        """
        path = [start]

        while path[-1] != goal:
            for direction in Direction:
                next_loc = path[-1].next(direction)
                if len(path) > 1 and next_loc == path[-2]:
                    continue  # Don't go back

                if not self.grid.in_range(next_loc):
                    continue  # Outside the grid

                if (
                    next_loc in self.grid.items
                    and self.grid.items[next_loc].character == "#"
                ):
                    continue  # Wall, skip

                path.append(next_loc)

        return path

    @staticmethod
    def find_any_cheats(
        maze_path: List[RowCol],
        cheat_duration: int,
        cheat_minimum: int,
    ) -> int:
        """Find the number of possible cheats.

        :param maze_path: List of steps in the original maze solution
        :param cheat_duration: The number of steps that a cheat may last
        :param cheat_minimum: The minimum amount of steps saved for a specific cheat
        """
        cheats = 0

        # Check all combinations of path elements for possible cheat options:
        for i_start, loc_start in enumerate(maze_path):
            # for i_end in range(i_start + cheat_minimum, len(maze_path)):
            for i_end in range(i_start + 2 + cheat_minimum, len(maze_path)):
                # Skip the items directly after `i_start`, as here we'll never
                # safe more than `cheat_minimum` steps
                loc_end = maze_path[i_end]

                this_cheat_distance = loc_start.distance(loc_end)
                if this_cheat_distance > cheat_duration:
                    continue  # Too far, we cannot cheat this

                this_physical_distance = i_end - i_start
                time_saved = this_physical_distance - this_cheat_distance
                if time_saved >= cheat_minimum:
                    cheats += 1

        return cheats


if __name__ == "__main__":
    main(Day20)
