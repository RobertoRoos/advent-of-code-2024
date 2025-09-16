import unittest

from advent_of_code.day_19.__main__ import Day19

from ..advent_testcase import AdventTestCase


class TestDay19(AdventTestCase):

    PUZZLE = Day19

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("6", result)

    def test_part_2_individual(self):
        solver: Day19 = self.get_solver(2)
        _ = solver()
        result = solver.possible_design("brwrr")
        self.assertEqual(2, result)
        result = solver.possible_design("bggr")
        self.assertEqual(1, result)
        result = solver.possible_design("gbbr")
        self.assertEqual(4, result)
        result = solver.possible_design("rrbgbr")
        self.assertEqual(6, result)
        result = solver.possible_design("bwurrg")
        self.assertEqual(1, result)
        result = solver.possible_design("brgr")
        self.assertEqual(2, result)
        result = solver.possible_design("ubwu")
        self.assertEqual(0, result)
        result = solver.possible_design("bbrgwb")
        self.assertEqual(0, result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("16", result)


if __name__ == "__main__":
    unittest.main()
