from typing import List, Set, Tuple, Dict
from collections import defaultdict

from advent_of_code.shared import Solver, main, Grid, GridItem, RowCol


class Day12(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.garden = Grid()

    def __call__(self) -> str:

        for line in self.iterate_input():
            self.garden.add_str_row(line)

        regions_by_char = self.find_regions()

        total_score = 0
        for char, regions in regions_by_char.items():
            for region in regions:
                this_score = self.calculate_score(region)
                total_score += this_score
                print(f"Region {char}: {this_score}")

        return str(total_score)

    def find_regions(self) -> defaultdict[str, List[Set[RowCol]]]:
        """Detect matching garden plots (= regions)."""
        # List of sets, each representing one region
        regions_by_char: defaultdict[str, List[Set[RowCol]]] = defaultdict(list)

        # Loop over all items:
        for loc, item in self.garden.items.items():
            # Loop over all the neighbouring items to find an existing region:
            this_region = None
            for neighbour in self.garden.neighbours(item):
                # Iterate over existing regions to find a match:
                for region in regions_by_char[item.character]:
                    if neighbour.loc in region:
                        this_region = region  # Reference to existing one
                        break

                if this_region is not None:
                    this_region.add(item.loc)
                    break  # Stop checking neighbours

            if this_region is None:
                # Start a new region then:
                regions_by_char[item.character].append({item.loc})

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
