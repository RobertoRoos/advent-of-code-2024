import unittest

from advent_of_code.day_21.__main__ import Day21, Keypad, KeypadType

from ..advent_testcase import AdventTestCase


class TestDay21(AdventTestCase):

    PUZZLE = Day21

    def test_samples(self):
        fixtures = {
            "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>"
            "AAvA^A<v<A>A>^AAAvA<^A>A",
            "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAv" "A<^A>A<vA>^A<A>A",
            "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^A"
            "A<A>A<v<A>A>^AAAvA<^A>A",
            "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<"
            "A>A<v<A>A>^AAvA<^A>A",
            "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A"
            ">A<v<A>A>^AAAvA<^A>A",
        }
        for code, expected in fixtures.items():
            pads = [
                Keypad(KeypadType.NUMERIC),
                Keypad(KeypadType.DIRECTIONAL),
                Keypad(KeypadType.DIRECTIONAL),
            ]
            min_length = Keypad.get_final_complexity_of_stack(pads, code)
            self.assertEqual(len(expected), min_length)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("126384", result)

    def test_other_answers_part_1(self):
        """Compare intermediate answers from a solution I saw online.

        I got so stuck here I didn't know what to do, so here we are comparing
        step-by-step values.
        """
        fixtures = {
            "169A": 76,
            "279A": 72,
            "540A": 72,
            "869A": 70,
            "789A": 66,
        }
        for code, expected in fixtures.items():
            pads = [
                Keypad(KeypadType.NUMERIC),
                Keypad(KeypadType.DIRECTIONAL),
                Keypad(KeypadType.DIRECTIONAL),
            ]
            min_len = Keypad.get_final_complexity_of_stack(pads, code)
            self.assertEqual(expected, min_len)

    # def test_sample_part_2(self):
    #     solver = self.get_solver(2)
    #     result = solver()
    #     self.assertEqual("xxx", result)


if __name__ == "__main__":
    unittest.main()
