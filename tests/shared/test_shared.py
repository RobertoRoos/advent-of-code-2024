import contextlib
import io
import unittest

from advent_of_code.shared import Grid, RowCol, Solver

from ..advent_testcase import AdventTestCase


class Day00(Solver):
    """Dummy puzzle implementation."""

    def __call__(self, *args, **kwargs):
        return 42


class TestDay00Bare(unittest.TestCase):

    def test_help(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit):
                _ = Day00(["--help"])

        txt = f.getvalue()
        self.assertTrue(txt.startswith("usage: "))


class TestDay00(AdventTestCase):

    PUZZLE = Day00

    def test_call(self):
        result = self.get_solver()()

        self.assertEqual(42, result)

    def test_input(self):
        obj = self.get_solver()
        txt = "\n".join(list(obj.iterate_input()))
        self.assertEqual("test\n", txt)


class TestGrid(unittest.TestCase):

    def test_grid_and_item(self):
        grid = Grid()
        for row in ["...", ".x.", "..."]:
            grid.add_str_row(row)

        self.assertEqual(1, len(grid.items))

        # Move an item and verify the index changes accordingly:
        robot = grid.get_item_by_character("x")
        robot.loc += RowCol(row=1, col=0)
        self.assertEqual(1, robot.loc.col)
        self.assertEqual(2, robot.loc.row)

        grid_keys = list(grid.items.keys())
        self.assertEqual([RowCol(row=2, col=1)], grid_keys)
        # This works because the key is actually a reference to the RowCol object

    def test_grid_maze_solution(self):
        grid = Grid()
        maze = """
########
#...#..#
#.S##..#
#.####.#
#......#
#####..#
#..E...#
########
"""
        for line in maze.split():
            grid.add_str_row(line.strip())

        start = grid.get_item_by_character("S")
        goal = grid.get_item_by_character("E")
        path_length, path = grid.find_path(start.loc, goal.loc)
        # grid.print_path(path)
        self.assertEqual(11, path_length)


if __name__ == "__main__":
    unittest.main()
