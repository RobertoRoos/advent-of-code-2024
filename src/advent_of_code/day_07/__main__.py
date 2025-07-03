from enum import Enum
from typing import List

from advent_of_code.shared import Solver, main


class Operator(Enum):
    add = "+"
    multiply = "*"


class Day07(Solver):

    def __call__(self) -> str:
        result = 0

        for line in self.iterate_input():
            total_str, _, numbers_str = line.strip().partition(":")

            total = int(total_str)
            numbers = [int(t) for t in numbers_str.strip().split(" ")]

            if self.possible_equation(total, numbers):
                result += total

        return str(result)

    @classmethod
    def possible_equation(cls, total: int, numbers: List[int]) -> bool:
        """Check if this equation can be completed."""
        size = len(numbers) - 1  # Number of operators
        for i in range(2**size):  # Systematically try all options:
            bin_format = "{:0" + str(size) + "b}"
            i_binary_str = bin_format.format(i)  # E.g. "6" becomes "000110"
            operators = [
                Operator.multiply if c == "1" else Operator.add for c in i_binary_str
            ]

            test_total = cls.do_multiple_operations(numbers, operators)
            if test_total == total:
                return True

        return False

    @classmethod
    def do_multiple_operations(cls, numbers: List[int], ops: List[Operator]) -> int:
        total = numbers[0]
        for number, op in zip(numbers[1:], ops):
            total = cls.do_operation(total, number, op)

        return total

    @staticmethod
    def do_operation(number_1: int, number_2: int, op: Operator) -> int:
        if op == Operator.add:
            return number_1 + number_2
        return number_1 * number_2


if __name__ == "__main__":
    main(Day07)
