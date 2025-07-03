from enum import Enum
from typing import List

from advent_of_code.shared import Solver, main


class Operator(Enum):
    ADD = "+"
    MULT = "*"
    CONCAT = "||"

    @classmethod
    def from_number(cls, number: str):
        if number == "0":
            return cls.ADD
        if number == "1":
            return cls.MULT
        return cls.CONCAT


class Day07(Solver):

    OPTIONS = [Operator.ADD, Operator.MULT]

    def __call__(self) -> str:
        result = 0

        if self.args.part == 2:
            Day07.OPTIONS.append(Operator.CONCAT)

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
        base = len(cls.OPTIONS)
        for i in range(base**size):  # Systematically try all options:
            i_based_str = cls.base_string(i, base)
            i_based_str = (size - len(i_based_str)) * "0" + i_based_str
            operators = [Operator.from_number(c) for c in i_based_str]

            if cls.test_multiple_operations(total, numbers, operators):
                return True

        return False

    @classmethod
    def test_multiple_operations(
        cls, expected: int, numbers: List[int], ops: List[Operator]
    ) -> int:
        """Return true if this operation series matches the expectation."""
        total = numbers[0]
        for number, op in zip(numbers[1:], ops):
            total = cls.do_operation(total, number, op)

            if total > expected:
                return False  # No need to continue, already done

        return total == expected

    @staticmethod
    def do_operation(number_1: int, number_2: int, op: Operator) -> int:
        if op == Operator.ADD:
            return number_1 + number_2
        if op == Operator.MULT:
            return number_1 * number_2
        return int(str(number_1) + str(number_2))

    @staticmethod
    def base_string(n, base) -> str:
        if n == 0:
            return "0"
        nums = []
        while n:
            n, r = divmod(n, base)
            nums.append(str(r))
        return "".join(reversed(nums))


if __name__ == "__main__":
    main(Day07)
