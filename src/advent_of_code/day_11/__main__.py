from typing import List

from advent_of_code.shared import Solver, main


class Day11(Solver):

    def __call__(self) -> str:
        stones: List[int] = []
        for line in self.iterate_input():
            stones = [int(t) for t in line.split(" ")]
            break

        for _ in range(25):  # 25 Blinks

            new_stones: List[int] = []  # New iteration of stones row

            for _, stone in enumerate(stones):
                new_stones += self.evolve_stone(stone)

            stones = new_stones

        return str(len(stones))

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
