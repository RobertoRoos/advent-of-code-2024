from collections import defaultdict
from typing import List, Self, Set

from advent_of_code.shared import Solver, main


class Page:
    """Page entity, so it can be sorted.

    We will rely on the default `sorted` function. We just need to implement a custom
    comparison method, which will rely on the page order information.
    """

    ORDER: defaultdict[int, Set[Self]] = defaultdict(set)
    # Like ``n: [list of numbers that may only follow n, not precede it]``

    def __init__(self, number: int | str):
        self.number = int(number) if isinstance(number, str) else number

    def __eq__(self, other: Self) -> bool:
        return self.number == other.number

    def __hash__(self) -> int:
        return self.number

    def __repr__(self) -> str:
        return f"<Page ({self.number})>"

    def __lt__(self, other: Self) -> bool:
        following = self.ORDER[self.number]
        if other in following:
            return True  # `other` must be after `self`, so `self` is less than `other`

        return False  # `other` has no relation to `self`, just return false


class Day05(Solver):

    def __call__(self) -> str:

        do_updates = False

        updates: List[List[Page]] = []

        for line in self.iterate_input():
            line = line.strip()
            if line == "":
                do_updates = True
                continue

            if not do_updates:
                page_1, _, page_2 = line.partition("|")
                page_1, page_2 = Page(page_1), Page(page_2)
                Page.ORDER[page_1.number].add(page_2)

            else:
                pages = [Page(t) for t in line.split(",")]
                updates.append(pages)

        value_part_1 = 0
        updates_invalid: List[List[Page]] = []

        for update in updates:
            if self.check_update_order(update):
                value_part_1 += self.get_middle(update).number
            else:
                updates_invalid.append(update)

        if self.args.part == 1:
            return str(value_part_1)

        value_part_2 = 0

        for update in updates_invalid:
            update_sorted = sorted(update)
            value_part_2 += self.get_middle(update_sorted).number

        return str(value_part_2)

    @staticmethod
    def get_middle(array: List[Page]) -> Page:
        middle_idx = int((len(array) - 1) / 2)
        return array[middle_idx]

    @staticmethod
    def check_update_order(update: List[Page]) -> bool:
        """Return True if an update (i.e. set of pages) is in a valid order.

        Loop over each number and than over all the numbers after. For each pair find
        the relevant rules and verify those rules.
        """

        for i, page in enumerate(update):

            for other_page in update[(i + 1) :]:
                following_pages = Page.ORDER[other_page.number]

                # If the first number must actually follow the second number, a rule
                # is violated and this is not a valid update:
                if page in following_pages:
                    return False

        return True


if __name__ == "__main__":
    main(Day05)
