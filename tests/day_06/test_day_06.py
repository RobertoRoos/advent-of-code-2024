import unittest

from advent_of_code.day_06.__main__ import Day06

from ..advent_testcase import AdventTestCase


class TestDay06(AdventTestCase):

    PUZZLE = Day06

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("41", result)

    def test_sample_part_1_custom(self):
        """The given sample is solved correctly but the real input isn't.

        So also try this custom sample:

            ..#....#..
            ..^>>>>#..
            ..^...v#..
            ......v...
            .....#v...
            .....^v>>>
            .....^v...
            ....#<v...
            ......#...
            ..........
        """
        solver = self.get_solver(1, input_file="sample_input_custom.txt")
        result = solver()
        self.assertEqual("18", result)

    def test_sample_part_1_custom_small(self):
        solver = self.get_solver(1, input_file="sample_input_custom_small.txt")
        result = solver()
        self.assertEqual("3", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("", result)


if __name__ == "__main__":
    unittest.main()
