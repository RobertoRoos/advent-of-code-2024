import unittest

from advent_of_code.day_15.__main__ import Day15
from advent_of_code.shared import Direction

from ..advent_testcase import AdventTestCase


class TestDay15(AdventTestCase):

    PUZZLE = Day15

    def test_sample_part_1_small(self):
        solver = self.get_solver(1, input_file="sample_input_small.txt")
        result = solver()
        self.assertEqual("2028", result)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("10092", result)

    def test_sample_part_2_small(self):
        solver = self.get_solver(2, input_file="sample_input_small_part_2.txt")
        result = solver()
        self.assertEqual("618", result)  # Counted by hand

    def test_find_item_chain_wide(self):
        solver: Day15 = self.get_solver(2)  # File isn't used here
        full_map = """####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##...[].......[]..##
##[]##....[]......##
##[]......[]..[]..##
##..[][]..@[].[][]##
##........[]......##
####################"""
        for line in full_map.split():
            solver.grid.add_str_row(line)

        solver.robot = solver.grid.get_item_by_character("@")

        to_be_moved = solver.find_item_chain(solver.robot, Direction.NORTH)

        self.assertEqual(5, len(to_be_moved))

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("9021", result)


if __name__ == "__main__":
    unittest.main()
