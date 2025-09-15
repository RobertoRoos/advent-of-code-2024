from typing import List

from advent_of_code.shared import Solver, main

Towel = str


class Day19(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stock: List[Towel] = []

    def __call__(self) -> str:

        designs: List[Towel] = []

        first_line = True
        for line in self.iterate_input():
            line = line.strip()

            if not line:
                first_line = False
                continue

            if first_line:
                # self.stock = [Color.towel_from_str(part) for part in line.split(",")]
                self.stock = [part.strip() for part in line.split(",")]
            else:
                # designs.append(Color.towel_from_str(line))
                designs.append(line.strip())

        number_possible = 0

        for design in designs:
            if self.possible_design(design):
                number_possible += 1

        return str(number_possible)

    def possible_design(self, design: Towel) -> bool:
        """Return True if a towel design can be made from the stock."""
        mixes: List[Towel] = [""]
        # Collection of lists of stock towels that might make the design - effectively
        # partial 'paths' through the network

        while mixes:
            # Take a 'path' from the 'queue' to pursue:
            mix = mixes.pop()  # < This is the design so far

            if mix == design:
                return True

            design_remaining = design[len(mix) :]

            for stock_towel in self.stock:
                if design_remaining.startswith(stock_towel):
                    mixes.append(mix + stock_towel)  # Next possible bit

        return False


if __name__ == "__main__":
    main(Day19)
