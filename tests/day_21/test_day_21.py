import unittest
from collections import defaultdict
from itertools import product

from advent_of_code.day_21.__main__ import Day21, Keypad, KeypadType

from ..advent_testcase import AdventTestCase


class TestDay21(AdventTestCase):

    PUZZLE = Day21

    def test_keypad_recursion(self):
        pads = [
            Keypad(KeypadType.NUMERIC),
            Keypad(KeypadType.DIRECTIONAL),
            Keypad(KeypadType.DIRECTIONAL),
        ]
        sequences = list(
            Keypad.consecutive_keypads(pads, "029A")
        )
        expected = [
            "029A",
            "<A^A>^^AvvvA",
            "v<<A>>^A<A>AvA<^AA>A<vAAA>^A",
            "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
        ]
        self.assertEqual(expected[1:], sequences)

    def test_keypad_finder(self):
        path = list(Keypad.find_keypad_directions(
            KeypadType.DIRECTIONAL,
            "^",
            ">"
        ))
        return

    # def test_keypad_finder(self):
    #
    #     pad = Keypad(Day21.KEYPAD_NUMERIC)
    #
    #     pad.move_to("7")
    #     buttons = pad.find_and_press_button("6")
    #     self.assertEqual("v>>A", buttons)
    #
    #     pad.move_to("7")
    #     buttons = pad.find_and_press_button("A")
    #     self.assertEqual("vv>v>A", buttons)
    #     # End with ">", not with "v"
    #
    #     pad.move_to("0")
    #     buttons = pad.find_and_press_button("7")
    #     self.assertEqual("^<^^A", buttons)
    #     # End with "^", not with "<"

    def test_find_all(self):
        pad = Keypad(Day21.KEYPAD_NUMERIC)
        paths = list(pad.find_all_keypad_direction_buttons("2"))
        self.assertEqual(2, len(paths))
        paths = list(pad.find_all_keypad_direction_buttons("3"))
        self.assertEqual(1, len(paths))
        paths = list(pad.find_all_keypad_direction_buttons("4"))
        self.assertEqual(5, len(paths))
        paths = list(pad.find_all_keypad_direction_buttons("7"))
        self.assertEqual(9, len(paths))

    def test_debugging(self):
        pad1 = Keypad(Day21.KEYPAD_NUMERIC)
        pad2 = Keypad(Day21.KEYPAD_DIRECTIONAL)
        pad3 = Keypad(Day21.KEYPAD_DIRECTIONAL)

        all_paths = []

        for path1 in pad1.find_all_keypad_direction_buttons("2"):
            for button1 in path1:
                for path2 in pad2.find_all_keypad_direction_buttons(button1):
                    for button2 in path2:
                        for path3 in pad3.find_all_keypad_direction_buttons(button2):
                            all_paths.append((path1, path2, path3))

        return

    def test_debugging_2(self):
        pad1 = Keypad(Day21.KEYPAD_DIRECTIONAL)
        pad2 = Keypad(Day21.KEYPAD_DIRECTIONAL)
        pad3 = Keypad(Day21.KEYPAD_DIRECTIONAL)

        all_paths = {}

        for button_from in Day21.KEYPAD_DIRECTIONAL.keys():
            for button_to in Day21.KEYPAD_DIRECTIONAL.keys():
                if button_to == button_from or button_to == "x" or button_from == "x":
                    continue

                all_paths[(button_from, button_to)] = {}

                pad1.move_to(button_from)
                for path1 in pad1.find_all_keypad_direction_buttons(button_to):
                    path1 += "A"

                    all_paths[(button_from, button_to)][path1] = {}

                    for path1_button in path1:

                        for path2 in pad2.find_all_keypad_direction_buttons(path1_button):
                            path2 += "A"

                            all_paths[(button_from, button_to)][path1][path2] = []

                            for path2_button in path2:

                                for path3 in pad3.find_all_keypad_direction_buttons(path2_button):
                                    path3 += "A"

                                    all_paths[(button_from, button_to)][path1][path2].append(path3)

                                pad3.move_to(path2_button)

                        pad2.move_to(path1_button)

                pass

        return

    def test_debugging_3(self):
        all_directional_paths = defaultdict(dict)

        pad = Keypad(Day21.KEYPAD_DIRECTIONAL)

        for button_from in Day21.KEYPAD_DIRECTIONAL.keys():
            for button_to in Day21.KEYPAD_DIRECTIONAL.keys():
                if button_to == "x" or button_from == "x":
                    continue

                pad.move_to(button_from)
                paths = []
                for path in pad.find_all_keypad_direction_buttons(button_to):
                    path += "A"
                    paths.append(path)

                all_directional_paths[button_from][button_to] = paths

        combinations_list = [
            paths
            for to in all_directional_paths.values()
            for paths in to.values()
        ]

        all_strategy_paths = []

        for strategy in product(*combinations_list):
            strategy_directional_paths = defaultdict(dict)
            i = 0
            for button_from, to_list in all_directional_paths.items():
                for button_to in to_list.keys():
                    strategy_directional_paths[button_from][button_to] = strategy[i]
                    i += 1
            all_strategy_paths.append(strategy_directional_paths)

        return

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
