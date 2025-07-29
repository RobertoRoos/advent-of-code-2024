from typing import List

from advent_of_code.shared import Grid, GridItem, RowCol, Solver, main


class Robot(GridItem):
    """Helper class to store info for each robot."""

    ROWS = 103
    COLS = 101

    def __init__(self):
        super().__init__()
        self.loc = RowCol(0, 0)
        self.character = "x"
        self.velocity = RowCol(0, 0)

    @staticmethod
    def from_str(line: str) -> "Robot":
        """Parse input string into robot instance."""
        values = []
        for part in line.strip().split(" "):
            _, _, value_str = part.partition("=")
            values.append(RowCol.from_str(value_str).transpose())
            # A bit awkward, but our row-column system is transposed:
            # x = col
            # y = row

        robot = Robot()
        robot.loc = values[0]
        robot.velocity = values[1]

        return robot

    def __repr__(self) -> str:
        return f"Robot({self.loc.row}, {self.loc.col})"

    def move(self, steps: int = 1):
        """Update position based on velocity for a numer of steps."""
        row = self.loc.row + steps * self.velocity.row
        col = self.loc.col + steps * self.velocity.col
        row = row % self.ROWS  # Mimic teleporting:
        col = col % self.COLS
        self.loc = RowCol(row=row, col=col)


class Day14(Solver):

    def __call__(self) -> str:

        robots: List[Robot] = [Robot.from_str(line) for line in self.iterate_input()]

        if self.args.part == 1:
            for robot in robots:
                robot.move(100)

            quadrants: List[int] = [0, 0, 0, 0]
            q1_row = (Robot.ROWS - 1) / 2
            q1_col = (Robot.COLS - 1) / 2

            for robot in robots:
                if robot.loc.row < q1_row and robot.loc.col < q1_col:
                    quadrants[0] += 1
                elif robot.loc.row < q1_row and robot.loc.col > q1_col:
                    quadrants[1] += 1
                elif robot.loc.row > q1_row and robot.loc.col < q1_col:
                    quadrants[2] += 1
                elif robot.loc.row > q1_row and robot.loc.col > q1_col:
                    quadrants[3] += 1

            score = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

        else:
            # I read by other solutions that when the Christmas trees shows, all roots
            # are in a unique position. So we just search for that instead.
            seconds = 0
            while True:
                for r in robots:
                    r.move()
                seconds += 1

                if self.positions_are_unique(robots):
                    # self.print(robots)
                    break
            score = seconds

        return str(score)

    @staticmethod
    def positions_are_unique(robots: List[Robot]) -> bool:
        unique_positions = set()
        for r in robots:
            if r.loc in unique_positions:
                return False
            unique_positions.add(r.loc)

        return True

    @staticmethod
    def print(robots: List[Robot]):
        grid = Grid()
        grid.rows = Robot.ROWS
        grid.cols = Robot.COLS
        for r in robots:
            grid.items[r.loc] = r

        grid.print()


if __name__ == "__main__":
    main(Day14)
