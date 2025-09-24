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
        self.assertEqual(expected[1:3], sequences[0:2])
        self.assertEqual(len(expected[3]), len(sequences[2]))
        # Our path is different, but same outcome

    def test_samples(self):
        fixtures = {
            "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
            "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
            "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
            "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
            "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
        }
        for code, expected in fixtures.items():
            pads = [
                Keypad(KeypadType.NUMERIC),
                Keypad(KeypadType.DIRECTIONAL),
                Keypad(KeypadType.DIRECTIONAL),
            ]
            sequences = list(
                Keypad.consecutive_keypads(pads, code)
            )
            self.assertEqual(len(expected), len(sequences[-1]))

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
