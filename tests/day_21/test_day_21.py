import unittest

from advent_of_code.day_21.__main__ import Day21, Keypad

from ..advent_testcase import AdventTestCase


class TestDay21(AdventTestCase):

    PUZZLE = Day21

    def test_keypad_finder(self):

        pad = Keypad(Day21.KEYPAD_NUMERIC)

        pad.move_to("7")
        buttons = pad.find_and_press_button("6")
        self.assertEqual("v>>A", buttons)

        pad.move_to("7")
        buttons = pad.find_and_press_button("A")
        self.assertEqual("vv>v>A", buttons)
        # End with ">", not with "v"

        pad.move_to("0")
        buttons = pad.find_and_press_button("7")
        self.assertEqual("^<^^A", buttons)
        # End with "^", not with "<"

    def test_consecutive_keypads(self):
        keypad_1 = Keypad(Day21.KEYPAD_NUMERIC)
        keypad_2 = Keypad(Day21.KEYPAD_DIRECTIONAL)
        keypad_3 = Keypad(Day21.KEYPAD_DIRECTIONAL)

        code = "029A"
        buttons = [code]
        buttons.append(
            keypad_1.find_button_series(buttons[-1])
        )
        buttons.append(
            keypad_2.find_button_series(buttons[-1])
        )
        buttons.append(
            keypad_3.find_button_series(buttons[-1])
        )

        expected = [
            "<A^A>^^AvvvA",
            "v<<A>>^A<A>AvA<^AA>A<vAAA>^A",
            "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
        ]

        # self.assertEqual(expected[0], buttons[1])
        self.assertEqual(len(expected[0]), len(buttons[1]))
        # self.assertEqual(expected[1], buttons[2])
        self.assertEqual(expected[1], buttons[2])
        self.assertEqual(expected[2], buttons[3])
        # self.assertEqual(68, len(buttons[3]))  # The order for me is different actually

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
