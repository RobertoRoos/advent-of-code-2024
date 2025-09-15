import unittest

from advent_of_code.day_18.__main__ import Day18

from ..advent_testcase import AdventTestCase


class TestDay18(AdventTestCase):

    PUZZLE = Day18

    def test_sample_part_1(self):
        """Map looks like:

        ```
            S..#...
            ..#..#.
            ....#..
            ...#..#
            ..#..#.
            .#..#..
            #.#...E
        ```
        """
        Day18.BYTE_LIMIT = 12  # Reduce limit for this sample
        Day18.GRID_SIZE = 6

        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("22", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
