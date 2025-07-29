from typing import List

from advent_of_code.shared import RowCol, Solver, main


class Robot:
    """Helper class to store info for each robot."""

    ROWS = 103
    COLS = 101

    def __init__(self):
        self.position = RowCol(0, 0)
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
        robot.position = values[0]
        robot.velocity = values[1]

        return robot

    def __repr__(self) -> str:
        return f"Robot({self.position.row}, {self.position.col})"

    def move(self, steps: int = 1):
        """Update position based on velocity for a numer of steps."""
        row = self.position.row + steps * self.velocity.row
        col = self.position.col + steps * self.velocity.col
        row = row % self.ROWS  # Mimic teleporting:
        col = col % self.COLS
        self.position = RowCol(row=row, col=col)


class Day14(Solver):

    def __call__(self) -> str:

        robots: List[Robot] = [Robot.from_str(line) for line in self.iterate_input()]

        for robot in robots:
            robot.move(100)

        quadrants: List[int] = [0, 0, 0, 0]
        q1_row = (Robot.ROWS - 1) / 2
        q1_col = (Robot.COLS - 1) / 2

        for robot in robots:
            if robot.position.row < q1_row and robot.position.col < q1_col:
                quadrants[0] += 1
            elif robot.position.row < q1_row and robot.position.col > q1_col:
                quadrants[1] += 1
            elif robot.position.row > q1_row and robot.position.col < q1_col:
                quadrants[2] += 1
            elif robot.position.row > q1_row and robot.position.col > q1_col:
                quadrants[3] += 1

        score = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

        return str(score)


if __name__ == "__main__":
    main(Day14)
