import unittest

from advent_of_code.day_07.__main__ import Day07

from ..advent_testcase import AdventTestCase


class TestDay01(AdventTestCase):

    PUZZLE = Day07

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("3749", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
