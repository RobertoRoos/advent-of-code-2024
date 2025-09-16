import unittest

from advent_of_code.day_20.__main__ import Day20

from ..advent_testcase import AdventTestCase


class TestDay01(AdventTestCase):

    PUZZLE = Day20

    def test_sample_part_1(self):
        Day20.CHEAT_MINIMUM = 1  # Disable limit
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("44", result)  # < All possible cheats

    def test_sample_part_2(self):
        Day20.CHEAT_MINIMUM = 50  # Change limit
        Day20.CHEAT_DURATION = 6  # Change ghost time
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("46", result)  # < Cheats that save at least 50 steps
        # It looks like the online sample might be wrong! The list doesn't match!


if __name__ == "__main__":
    unittest.main()
