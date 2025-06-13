import unittest

from advent_of_code.day_03.__main__ import Day03

from ..advent_testcase import AdventTestCase


class TestDay03(AdventTestCase):

    PUZZLE = Day03

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("161", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2, input_file="sample_input_2.txt")
        result = solver()
        self.assertEqual("48", result)


if __name__ == "__main__":
    unittest.main()
