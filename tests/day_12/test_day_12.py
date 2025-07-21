import unittest

from advent_of_code.day_12.__main__ import Day12
from advent_of_code.shared import Grid

from ..advent_testcase import AdventTestCase


class TestDay12(AdventTestCase):

    PUZZLE = Day12

    def test_sample_part_1_small(self):
        solver = self.get_solver(1, input_file="sample_input_small.txt")
        result = solver()
        self.assertEqual("140", result)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("1930", result)

    def test_sample_part_2_corners(self):

        fixture = [
            # (4 * 4, ["AAAA"]),
            (4 * 4, ["BB", "BB"]),
        ]
        for expected, lines in fixture:
            garden = Grid()
            for line in lines:
                garden.add_str_row(line)

            region = set(garden.items.keys())
            score = Day12.calculate_score_edges(region)
            self.assertEqual(expected, score)

    def test_sample_part_2_small(self):
        solver = self.get_solver(2, input_file="sample_input_small.txt")
        result = solver()
        self.assertEqual("80", result)

    def test_sample_part_2_letter_e(self):
        solver = self.get_solver(2, input_file="sample_input_E.txt")
        result = solver()
        self.assertEqual("236", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("1206", result)


if __name__ == "__main__":
    unittest.main()
