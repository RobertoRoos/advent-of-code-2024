import unittest

from advent_of_code.day_17.__main__ import Day17, Machine

from ..advent_testcase import AdventTestCase


class TestDay17(AdventTestCase):

    PUZZLE = Day17

    def test_machine_1(self):
        machine = Machine(0, 0, 9)
        machine.do_program([2, 6])
        self.assertEqual(1, machine.b)

    def test_machine_2(self):
        machine = Machine(10, 0, 0)
        machine.do_program([5, 0, 5, 1, 5, 4])
        self.assertEqual([0, 1, 2], machine.output)

    def test_machine_3(self):
        machine = Machine(2024, 0, 0)
        machine.do_program([0, 1, 5, 4, 3, 0])
        self.assertEqual([4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0], machine.output)
        self.assertEqual(0, machine.a)

    def test_machine_4(self):
        machine = Machine(0, 29, 0)
        machine.do_program([1, 7])
        self.assertEqual(26, machine.b)

    def test_machine_5(self):
        machine = Machine(0, 2024, 43690)
        machine.do_program([4, 0])
        self.assertEqual(44354, machine.b)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("4,6,3,5,6,3,5,2,1,0", result)

    def test_part_2_sample(self):
        solver = self.get_solver(2, input_file="sample_input_part_2.txt")
        result = solver()
        self.assertEqual("117440", result)

    def test_part_2_my_input(self):
        machine = Machine()
        program = [2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 2, 5, 5, 3, 0]
        _ = machine.find_circular_program(program)
        output = machine.do_program(program)
        self.assertEqual(program, output)


if __name__ == "__main__":
    unittest.main()
