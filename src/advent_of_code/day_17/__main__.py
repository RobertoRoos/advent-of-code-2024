from enum import IntEnum
from typing import List

from advent_of_code.shared import Solver, main


class Instruction(IntEnum):
    adv = 0  # division
    bxl = 1  # bitwise XOR
    bst = 2  # combo
    jnz = 3  # jump
    bxc = 4  # bitwise XOR
    out = 5  # combo
    bdv = 6  # division
    cdv = 7  # division


class Machine:
    """Abstraction for an instructions machine."""

    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c

        self.output: None | List[int] = None

    def do_program(self, program: List[int]) -> List[int]:
        self.output = []
        index = 0
        while index < len(program):
            index = self.do_instruction(index, program[index], program[index + 1])

        return self.output

    def get_combo_value(self, combo_opcode) -> int:
        if 0 <= combo_opcode <= 3:
            return combo_opcode
        elif combo_opcode == 4:
            return self.a
        elif combo_opcode == 5:
            return self.b
        elif combo_opcode == 6:
            return self.c
        else:
            raise ValueError(f"Invalid combo operand opcode ({combo_opcode})")

    def do_instruction(
        self, index: int, instruction_opcode: int, operand_opcode: int
    ) -> int:
        """Perform an instruction in this machine.

        Return the updated index."""
        if (
            instruction_opcode == Instruction.adv
            or instruction_opcode == Instruction.bdv
            or instruction_opcode == Instruction.cdv
        ):

            combo_value = self.get_combo_value(operand_opcode)
            result = self.a / (2**combo_value)
            result = int(result)

            if instruction_opcode == Instruction.adv:
                self.a = result
            elif instruction_opcode == Instruction.bdv:
                self.b = result
            else:
                self.c = result

        elif instruction_opcode == Instruction.bxl:
            self.b = self.b ^ operand_opcode

        elif instruction_opcode == Instruction.bst:
            combo_value = self.get_combo_value(operand_opcode)
            self.b = combo_value % 8

        elif instruction_opcode == Instruction.jnz:
            if self.a != 0:
                return operand_opcode  # Jump!

        elif instruction_opcode == Instruction.bxc:
            self.b = self.b ^ self.c

        elif instruction_opcode == Instruction.out:
            combo_value = self.get_combo_value(operand_opcode)
            self.output.append(combo_value % 8)

        return index + 2  # Default increment

    def find_circular_program(self, program: List[int]) -> int:
        """Find value for `a` such that output equals the program itself.

        We see a pattern that for `a = 8^n` the output has `n + 1` items,
        regardless of the program.
        Also, each 'octo-bit' in `a` will change only one or two values in the output
        list. So to converge to a solution, we find the last digit in the output
        and the program that are different and then increment `a` with the right
        exponent of 8.
        """
        # Find the lowest meaningful value for register `a`:
        n = 0
        output = []
        while len(output) < len(program):
            self.a = 8**n
            output = Machine(self.a, self.b, self.c).do_program(program)
            n += 1

        # Increment `a` according to the last element that's different:
        pos = len(program) - 1
        while output != program:
            # Find last digit to adjust:
            for pos in range(len(program) - 1, -1, -1):
                if program[pos] != output[pos]:
                    break

            self.a += 8**pos  # Increment the octo-bit of this position

            output = Machine(self.a, self.b, self.c).do_program(program)

            if len(output) > len(program):
                raise RuntimeError("Not converging to solution")

        return self.a


class Day17(Solver):

    def __call__(self) -> str:

        reading_registers = True
        registers: List[int] = []
        program: List[int] = []
        for line in self.iterate_input():
            if not line:
                reading_registers = False
                continue

            if reading_registers:
                _, _, number = line.partition(": ")
                registers.append(int(number))
            else:
                _, _, numbers_str = line.partition(": ")
                program = [int(txt) for txt in numbers_str.split(",")]

        machine = Machine(*registers)

        if self.args.part == 1:
            output = machine.do_program(program)
            return ",".join(str(t) for t in output)
        else:
            machine.find_circular_program(program)
            return str(machine.a)


if __name__ == "__main__":
    main(Day17)
