import unittest

from advent_of_code.day_09.__main__ import Day09

from ..advent_testcase import AdventTestCase


class TestDay09(AdventTestCase):

    PUZZLE = Day09

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("1928", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("2858", result)


if __name__ == "__main__":
    unittest.main()
