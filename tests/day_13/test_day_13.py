import unittest

from advent_of_code.day_13.__main__ import Day13

from ..advent_testcase import AdventTestCase


class TestDay13(AdventTestCase):

    PUZZLE = Day13

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("480", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
