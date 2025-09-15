from typing import Dict, List, Tuple, Set

from advent_of_code.shared import (
    Direction,
    Grid,
    GridItem,
    PriorityList,
    RowCol,
    Solver,
    main,
)

Path = List[RowCol]


class Day18(Solver):

    BYTE_LIMIT = 1024
    GRID_SIZE = 70  # Grid size (inclusive)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = Grid()
        self.grid.rows = self.GRID_SIZE + 1
        self.grid.cols = self.GRID_SIZE + 1

    def __call__(self) -> str:

        i = 0
        obstacles: List[GridItem] = []
        for line in self.iterate_input():
            coord_x, _, coord_y = line.strip().partition(",")
            coord_x, coord_y = int(coord_x), int(coord_y)
            item = GridItem(loc=RowCol(coord_y, coord_x), character="#")
            obstacles.append(item)

        start = RowCol(0, 0)
        goal = RowCol(self.GRID_SIZE, self.GRID_SIZE)

        if self.args.part == 1:
            for i in range(self.BYTE_LIMIT):
                self.grid.add(obstacles[i])

            result, _ = self.find_shorest_path(start, goal)
            return str(result)

        else:
            path_so_far = None
            for _index, obstacle in enumerate(obstacles):
                self.grid.add(obstacle)

                if path_so_far is not None and obstacle.loc not in path_so_far:
                    continue  # No need to check validity, already walking around it

                if not self.check_possible_path(start, goal):
                    return f"{obstacle.loc.col},{obstacle.loc.row}"  # X,Y vs row,col

            raise RuntimeError("Couldn't find limiting block!")

    def find_shorest_path(self, start: RowCol, goal: RowCol) -> Tuple[int, Path]:
        """Return length of the shortest path through the maze.

        Uses a kind of Dijkstras, with a sorted queue.
        """
        path_queue = PriorityList[Path]()
        path_queue.push(0, [start])  # Path 'tips', prioritized by length so far

        best_distances: Dict[RowCol, int] = {}  # Map of shortest route to a location

        while path_queue:
            this_distance, this_path = path_queue.pop()
            this_tip = this_path[-1]

            if this_tip == goal:
                return this_distance, this_path

            # Investigate next paths:
            for direction in Direction:
                next_tip = this_tip.next(direction)
                if not self.walkable(next_tip):
                    continue

                next_distance = this_distance + 1

                if (
                    next_tip not in best_distances
                    or next_distance < best_distances[next_tip]
                ):
                    best_distances[next_tip] = next_distance
                    path_queue.push(next_distance, this_path[:] + [next_tip])

        raise RuntimeError("Failed to find solution")

    def check_possible_path(self, start: RowCol, goal: RowCol) -> bool:
        """Simplified pathfinder - return False if no path exists."""
        reachable_tiles: Set[RowCol] = set()
        tips: Set[RowCol] = {start}  # "Boundary" of new locations

        while tips:
            reachable_tiles |= tips

            new_tips: Set[RowCol] = set()

            for tip in tips:
                for direction in Direction:
                    new_tip = tip.next(direction)
                    if not self.walkable(new_tip):
                        continue

                    if new_tip not in reachable_tiles:
                        new_tips.add(new_tip)

            tips = new_tips

        return goal in reachable_tiles

    def walkable(self, loc: RowCol) -> bool:
        if not self.grid.in_range(loc):
            return False  # Out of bounds

        if loc in self.grid.items:
            if self.grid.items[loc].character == "#":
                return False  # Wall, skip this one

        return True

    def print_path(self, path: Path):
        path_grid = Grid()
        path_grid.rows = self.grid.rows
        path_grid.cols = self.grid.cols

        for step in path:
            path_grid.add(GridItem(step, "x"))

        print()
        path_grid.print()
        print()


if __name__ == "__main__":
    main(Day18)
