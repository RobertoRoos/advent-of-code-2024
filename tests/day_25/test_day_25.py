import unittest

from advent_of_code.day_25.__main__ import Day25

from ..advent_testcase import AdventTestCase


class TestDay25(AdventTestCase):

    PUZZLE = Day25

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("3", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        # There is no part 2 at all:
        self.assertEqual("<empty>", result)


if __name__ == "__main__":
    unittest.main()
