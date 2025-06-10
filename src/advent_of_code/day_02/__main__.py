from typing import List

from advent_of_code.shared import Solver, main


class Day02(Solver):

    def __call__(self) -> str:

        count_safe = 0
        for line in self.iterate_input():
            numbers = [int(txt) for txt in line.split(" ")]

            tolerance = 0 if self.args.part == 1 else 1

            if self.check_report(numbers):
                count_safe += 1
                continue

            if tolerance > 0:
                tolerated = False
                for i, _ in enumerate(numbers):
                    # Just brute-force trying to remove any and all numbers
                    # Not very nice, but it's plenty fast here
                    numbers_tolerated = [n for n in numbers]
                    numbers_tolerated.pop(i)
                    if self.check_report(numbers_tolerated):
                        tolerated = True
                        break

                if tolerated:
                    count_safe += 1

        return str(count_safe)

    @staticmethod
    def check_report(numbers: List[int]) -> bool:
        """Return true if report is safe."""
        diffs = [n2 - n1 for n1, n2 in zip(numbers[0:-1], numbers[1:])]

        positives = [d > 0 for d in diffs]
        if any(positives) and not all(positives):
            return False  # Not all are either decreasing or increasing

        margins = [1 <= abs(d) <= 3 for d in diffs]

        if not all(margins):
            return False  # Not all within range

        return True


if __name__ == "__main__":
    main(Day02)
