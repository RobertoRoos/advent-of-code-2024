from typing import List

from advent_of_code.shared import Solver, main


class Day01(Solver):

    def __call__(self) -> str:
        column_left: List[int] = []
        column_right: List[int] = []
        for line in self.iterate_input():
            left, _, right = line.partition(" ")
            column_left.append(int(left))
            column_right.append(int(right))

        column_left = sorted(column_left)
        column_right = sorted(column_right)

        if self.args.part == 1:

            sum_distance = 0
            for left, right in zip(column_left, column_right):
                sum_distance += abs(right - left)

            return str(sum_distance)

        else:

            column_right_counts = {v: column_right.count(v) for v in column_right}

            score = 0

            for val in column_left:
                score += val * column_right_counts.get(val, 0)

            return str(score)


if __name__ == "__main__":
    main(Day01)
