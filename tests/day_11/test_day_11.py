import unittest

from advent_of_code.day_11.__main__ import Day11

from ..advent_testcase import AdventTestCase


class TestDay11(AdventTestCase):

    PUZZLE = Day11

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("55312", result)

    # Part 2 has no known sample output!


if __name__ == "__main__":
    unittest.main()
