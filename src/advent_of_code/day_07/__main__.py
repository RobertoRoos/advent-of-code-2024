from enum import Enum
from typing import List, Tuple

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
    def possible_equation(
        cls,
        total: int,
        numbers: List[int],
        operators: List[Operator] | None = None,
        total_backwards: int = 0,
    ) -> bool:
        """Recursively check the possibility of an equation.

        Each execution branch will trigger new child execution branches, until the set
        of operands is full and it finally returns.
        We check the opposite action of each operation to see if we need to keep
        pursuing a particular branch. E.g. for "190: 10 19" we could never use
        concatenate to make the answer, regardless of what comes before.

        :param total:
        :param numbers:
        :param operators:   Recursive element
                            These are the last operators of this branch of execution
        :param total_backwards: Result with the operators we have already
        """
        if operators is None:
            operators = []
            total_backwards = total

        progress = len(operators)

        if progress == len(numbers) - 1:
            return numbers[0] == total_backwards

        if progress >= len(numbers):
            raise ValueError("Too many operators for this set of numbers!")

        # Not yet done, figure out the next possible operators, by working
        # the sum backwards:
        next_options: List[Tuple[Operator, int]] = []

        next_number_idx = len(numbers) - 1 - progress  # Number for the next operator
        next_number = numbers[next_number_idx]

        if Operator.CONCAT in cls.OPTIONS:
            total_backwards_str = str(total_backwards)
            next_number_str = str(next_number)
            if total_backwards != next_number and total_backwards_str.endswith(
                next_number_str
            ):
                total_backwards_next_str = total_backwards_str[: -len(next_number_str)]
                next_options.append((Operator.CONCAT, int(total_backwards_next_str)))

        if Operator.MULT in cls.OPTIONS:
            if total_backwards % next_number == 0:
                next_options.append((Operator.MULT, int(total_backwards / next_number)))

        if Operator.ADD in cls.OPTIONS:
            if total_backwards > next_number:
                next_options.append((Operator.ADD, total_backwards - next_number))

        for option, next_total_backwards in next_options:
            next_operations = [option] + operators[:]
            if cls.possible_equation(
                total, numbers, next_operations, next_total_backwards
            ):
                return True

        return False


if __name__ == "__main__":
    main(Day07)
