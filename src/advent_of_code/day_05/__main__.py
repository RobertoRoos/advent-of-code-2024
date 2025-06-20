from collections import defaultdict
from typing import List, Set

from advent_of_code.shared import Solver, main


class Day05(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.page_orders: defaultdict[int, Set[int]] = defaultdict(set)
        # Like ``n: [list of numbers that may only follow n, not precede it]``

    def __call__(self) -> str:

        do_updates = False

        updates: List[List[int]] = []

        for line in self.iterate_input():
            line = line.strip()
            if line == "":
                do_updates = True
                continue

            if not do_updates:
                number_1, _, number_2 = line.partition("|")
                number_1, number_2 = int(number_1), int(number_2)
                self.page_orders[int(number_1)].add(int(number_2))

            else:
                numbers = [int(t) for t in line.split(",")]
                updates.append(numbers)

        value = 0

        for update in updates:
            if self.check_update_order(update):
                middle_idx = int((len(update) - 1) / 2)
                value += update[middle_idx]

        return str(value)

    def check_update_order(self, update: List[int]) -> bool:
        """Return True if an update (i.e. set of pages) is in a valid order.

        Loop over each number and than over all the numbers after. For each pair find
        the relevant rules and verify those rules.
        """

        for i, number in enumerate(update):

            for other_number in update[(i + 1) :]:
                following_numbers = self.page_orders[other_number]

                # If the first number must actually follow the second number, a rule
                # is violated and this is not a valid update:
                if number in following_numbers:
                    return False

        return True


if __name__ == "__main__":
    main(Day05)
