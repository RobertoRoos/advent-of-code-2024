import unittest

from advent_of_code.day_04.__main__ import Day04

from ..advent_testcase import AdventTestCase


class TestDay04(AdventTestCase):

    PUZZLE = Day04

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("18", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("9999", result)


if __name__ == "__main__":
    unittest.main()
