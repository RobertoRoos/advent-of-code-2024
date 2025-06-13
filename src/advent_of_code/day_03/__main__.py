import re

from advent_of_code.shared import Solver, main


class Day03(Solver):

    RE_MULT = re.compile(r"mul\((\d+),(\d+)\)")
    RE_MULT_ENABLE = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")

    def __call__(self) -> str:
        txt = "\n".join(self.get_input())

        result = 0

        if self.args.part == 1:

            for match in self.RE_MULT.finditer(txt):
                result += int(match.group(1)) * int(match.group(2))

        else:

            enabled = True

            for match in self.RE_MULT_ENABLE.finditer(txt):
                if match.group(0) == "do()":
                    enabled = True
                elif match.group(0) == "don't()":
                    enabled = False
                elif match.group(0).startswith("mul"):
                    if enabled:
                        result += int(match.group(1)) * int(match.group(2))

        return str(result)


if __name__ == "__main__":
    main(Day03)
