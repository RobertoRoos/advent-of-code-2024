import unittest

from advent_of_code.day_12.__main__ import Day12

from ..advent_testcase import AdventTestCase


class TestDay12(AdventTestCase):

    PUZZLE = Day12

    def test_sample_part_1_small(self):
        solver = self.get_solver(1, input_file="sample_input_small.txt")
        result = solver()
        self.assertEqual("140", result)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("1930", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
