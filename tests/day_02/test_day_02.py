import unittest

from advent_of_code.day_02.__main__ import Day02

from ..advent_testcase import AdventTestCase


class TestDay02(AdventTestCase):

    PUZZLE = Day02

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("2", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("4", result)


if __name__ == "__main__":
    unittest.main()
