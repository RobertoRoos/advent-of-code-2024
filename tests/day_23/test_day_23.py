import unittest

from advent_of_code.day_23.__main__ import Day23

from ..advent_testcase import AdventTestCase


class TestDay23(AdventTestCase):

    PUZZLE = Day23

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("7", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
