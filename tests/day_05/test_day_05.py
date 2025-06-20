import unittest

from advent_of_code.day_05.__main__ import Day05

from ..advent_testcase import AdventTestCase


class TestDay05(AdventTestCase):

    PUZZLE = Day05

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("143", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("", result)


if __name__ == "__main__":
    unittest.main()
