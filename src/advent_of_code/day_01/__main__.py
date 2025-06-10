from advent_of_code.shared import Tool, main

from typing import List, Tuple


class Day01(Tool):

    def __call__(self) -> str:
        column_left: List[int] = []
        column_right: List[int] = []
        for line in self.iterate_input():
            left, _, right = line.partition(" ")
            column_left.append(int(left))
            column_right.append(int(right))

        column_left = sorted(column_left)
        column_right = sorted(column_right)

        sum_distance = 0
        for left, right in zip(column_left, column_right):
            sum_distance += abs(right - left)

        return str(sum_distance)


if __name__ == "__main__":
    main(Day01)
