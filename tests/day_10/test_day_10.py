import unittest

from advent_of_code.day_10.__main__ import Day10

from ..advent_testcase import AdventTestCase


class TestDay10(AdventTestCase):

    PUZZLE = Day10

    def test_sample_part_1_small(self):
        solver = self.get_solver(1, input_file="sample_input_small.txt")
        result = solver()
        self.assertEqual("3", result)

    def test_sample_part_1_loops(self):
        solver = self.get_solver(1, input_file="sample_input_loops.txt")
        result = solver()
        self.assertEqual("2", result)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("36", result)

    def test_sample_part_1_modified(self):
        solver = self.get_solver(1, input_file="sample_input_modified.txt")
        result = solver()
        self.assertEqual("5", result)

    def test_sample_part_2_small(self):
        solver = self.get_solver(2, input_file="sample_input_part_2_small.txt")
        result = solver()
        self.assertEqual("3", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("81", result)


if __name__ == "__main__":
    unittest.main()
