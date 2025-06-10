from advent_of_code.shared import Solver, main


class Day02(Solver):

    def __call__(self) -> str:

        count_safe = 0

        for line in self.iterate_input():
            numbers = [int(txt) for txt in line.split(" ")]
            diffs = [n2 - n1 for n1, n2 in zip(numbers[0:-1], numbers[1:])]

            positives = [d > 0 for d in diffs]
            if any(positives) and not all(positives):
                continue  # Not all are either decreasing or increasing

            margins = [1 <= abs(d) <= 3 for d in diffs]

            if not all(margins):
                continue  # Not all within range

            count_safe += 1  # No exceptions hit

        return str(count_safe)


if __name__ == "__main__":
    main(Day02)
