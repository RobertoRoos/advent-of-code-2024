import unittest

from advent_of_code.day_01.__main__ import Day01

from ..advent_testcase import AdventTestCase


class TestDay01(AdventTestCase):

    PUZZLE = Day01

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("11", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("31", result)


if __name__ == "__main__":
    unittest.main()
