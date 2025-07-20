from collections import defaultdict
from typing import List

from advent_of_code.shared import Solver, main

StonesDict = defaultdict[int, int]


class Day11(Solver):

    def __call__(self) -> str:

        # The order of the stones doesn't matter and the number of unique
        # ones isn't so great, so just keep a count of each value instead
        stones: StonesDict = defaultdict(lambda: 0)
        # Like: {"stone": "count"}

        for line in self.iterate_input():
            for stone in [int(t) for t in line.split(" ")]:
                stones[stone] += 1
            break

        number_of_blinks = 25 if self.args.part == 1 else 75

        for _ in range(number_of_blinks):

            new_stones: StonesDict = defaultdict(lambda: 0)

            for stone, count in stones.items():
                for this_new_stone in self.evolve_stone(stone):
                    # Tally the new stone(s) value(s) in the list
                    new_stones[this_new_stone] += count

            stones = new_stones

        stone_count = sum(stones.values())

        return str(stone_count)

    @staticmethod
    def evolve_stone(stone: int) -> List[int]:
        """Evolve a single stone, result is one new or two new."""
        if stone == 0:
            return [1]

        stone_str = str(stone)
        if len(stone_str) % 2 == 0:  # Even number of digits
            k = int(len(stone_str) / 2)
            return [int(stone_str[:k]), int(stone_str[k:])]

        return [stone * 2024]


if __name__ == "__main__":
    main(Day11)
