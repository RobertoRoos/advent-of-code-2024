import unittest

from advent_of_code.day_21.__main__ import Day21, Keypad

from ..advent_testcase import AdventTestCase


class TestDay21(AdventTestCase):

    PUZZLE = Day21

    def test_keypad_finder(self):

        pad = Keypad(Day21.KEYPAD_NUMERIC)

        pad.move_to("7")
        buttons = pad.find_directional_keypad_presses("6")
        self.assertEqual("v>>A", buttons)

        pad.move_to("7")
        buttons = pad.find_directional_keypad_presses("A")
        self.assertEqual(">>vvvA", buttons)
        # Make sure we don't unnecessarily mix vertical / horizontal!

        pad.move_to("0")
        buttons = pad.find_directional_keypad_presses("7")
        self.assertEqual("^^^<A", buttons)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("126384", result)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
