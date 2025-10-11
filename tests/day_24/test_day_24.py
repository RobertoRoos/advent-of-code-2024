import unittest

from advent_of_code.day_24.__main__ import Day24

from ..advent_testcase import AdventTestCase


class TestDay24(AdventTestCase):

    PUZZLE = Day24

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("4", result)

    def test_sample_part_1_larger(self):
        solver = self.get_solver(1, input_file="sample_input_larger.txt")
        result = solver()
        self.assertEqual("2024", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
