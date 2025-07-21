from collections import defaultdict
from typing import List, Set

from advent_of_code.shared import Grid, RowCol, Solver, main


class Day12(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.garden = Grid()

    def __call__(self) -> str:

        for line in self.iterate_input():
            self.garden.add_str_row(line)

        regions_by_char = self.find_regions()

        total_score = 0
        for regions in regions_by_char.values():
            for region in regions:
                this_score = self.calculate_score(region)
                total_score += this_score

        return str(total_score)

    def find_regions(self) -> defaultdict[str, List[Set[RowCol]]]:
        """Detect matching garden plots (= regions)."""
        # List of sets, each representing one region
        regions_by_char: defaultdict[str, List[Set[RowCol]]] = defaultdict(list)

        unsorted_locs = {it.loc for it in self.garden.items.values()}  # Make copy

        while len(unsorted_locs) > 0:  # Consume entire list
            this_loc = next(iter(unsorted_locs))
            this_item = self.garden.items[this_loc]

            region_dict = self.garden.find_region(this_item)
            region_set = set(region_dict.keys())
            unsorted_locs -= region_set

            regions_by_char[this_item.character].append(region_set)

        return regions_by_char

    @staticmethod
    def calculate_score(region: Set[RowCol]) -> int:
        """Get the numerical score of a garden region."""
        area = len(region)

        perimeter = 0

        for loc in region:
            for neighbour_loc in loc.neighbours():
                if neighbour_loc not in region:
                    perimeter += 1

        return area * perimeter


if __name__ == "__main__":
    main(Day12)
