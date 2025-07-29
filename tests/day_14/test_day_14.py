import unittest

from advent_of_code.day_14.__main__ import Day14, Robot
from advent_of_code.shared import RowCol

from ..advent_testcase import AdventTestCase


class TestDay14(AdventTestCase):

    PUZZLE = Day14

    def setUp(self):
        Robot.ROWS = 7
        Robot.COLS = 11

    def test_move(self):
        robot = Robot.from_str("p=2,4 v=2,-3")
        self.assertEqual(RowCol(row=4, col=2), robot.loc)
        robot.move()
        self.assertEqual(RowCol(row=1, col=4), robot.loc)
        robot.move()
        self.assertEqual(RowCol(row=5, col=6), robot.loc)

        robot = Robot.from_str("p=2,4 v=2,-3")
        robot.move(5)
        self.assertEqual(RowCol(row=3, col=1), robot.loc)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("12", result)

    # Nothing to test for part 2


if __name__ == "__main__":
    unittest.main()
