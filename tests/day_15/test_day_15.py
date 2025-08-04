import unittest

from advent_of_code.day_15.__main__ import Day15

from ..advent_testcase import AdventTestCase


class TestDay15(AdventTestCase):

    PUZZLE = Day15

    def test_sample_part_1_small(self):
        solver = self.get_solver(1, input_file="sample_input_small.txt")
        result = solver()
        self.assertEqual("2028", result)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("10092", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
