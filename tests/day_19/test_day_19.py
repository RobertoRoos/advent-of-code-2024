import unittest

from advent_of_code.day_19.__main__ import Day19

from ..advent_testcase import AdventTestCase


class TestDay19(AdventTestCase):

    PUZZLE = Day19

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("6", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
