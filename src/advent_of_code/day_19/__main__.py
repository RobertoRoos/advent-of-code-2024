from typing import Dict, Iterable, List, Set

from advent_of_code.shared import Solver, main

Towel = str


class Day19(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stock: Set[Towel] = set()
        self.stock_lookup = {}
        self.stock_max = 0

    def __call__(self) -> str:

        designs: List[Towel] = []

        first_line = True
        for line in self.iterate_input():
            line = line.strip()

            if not line:
                first_line = False
                continue

            if first_line:
                for part in line.split(","):
                    part = part.strip()
                    self.stock.add(part)
                    self.stock_max = max(self.stock_max, len(part))
            else:
                # designs.append(Color.towel_from_str(line))
                designs.append(line.strip())

        result = 0

        if self.args.part == 1:
            for design in designs:
                if self.possible_design(design) > 0:
                    result += 1

        else:
            for design in designs:
                result += self.possible_design(design)

        return str(result)

    def possible_design(self, design: Towel) -> int:
        """Return number of possible designs.

        Use the early return argument to check for any possibility at all.

        We work by tracking how many concurrent options there are for sub-designs of
        increasing length. This way we don't need to track multiple ways of making
        partially completed designs, but we just count them.
        """
        options_so_far: Dict[int, int] = {0: 1}
        # Like: `{ <# of colors so far>: <# of options for it, ... }
        # Collection of how many options there are for these number of colours pinned
        # already

        options = 0

        while options_so_far:
            # Take a 'path' from the 'queue' to pursue:
            option_length = next(iter(options_so_far))
            option_count = options_so_far.pop(option_length)

            if option_length == len(design):
                if self.args.part == 1:  # Just return on the first already
                    return 1
                else:
                    options += option_count
                    continue

            design_remaining = design[option_length:]

            for stock_option in self.find_stock_towel(design_remaining):
                new_length = option_length + len(stock_option)
                if new_length not in options_so_far:
                    options_so_far[new_length] = option_count
                else:
                    options_so_far[new_length] += option_count

        return options

    def find_stock_towel(self, pattern: Towel) -> Iterable[Towel]:
        """Yield the matching stock towels to the start of the given pattern."""
        i_max = min(self.stock_max, len(pattern)) + 1
        for i in range(1, i_max):
            substr = pattern[:i]
            if substr in self.stock:
                yield substr


if __name__ == "__main__":
    main(Day19)
