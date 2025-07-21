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
        for _, regions in regions_by_char.items():
            for region in regions:
                if self.args.part == 1:
                    this_score = self.calculate_score(region)
                else:
                    this_score = self.calculate_score_edges(region)
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
        """Get the numerical score of a garden region (part 1)."""
        area = len(region)

        perimeter = 0

        for loc in region:
            for neighbour_loc in loc.neighbours():
                if neighbour_loc not in region:
                    perimeter += 1
                    # Every neighbouring location that is not in this region
                    # (or outside the grid) represents a plot edge!

        return area * perimeter

    @staticmethod
    def calculate_score_edges(region: Set[RowCol]) -> int:
        """Get the numerical score of a garden region (part 2)."""
        area = len(region)

        corners = 0  # The number of corners of the shape is also the number
        # of outer edges!

        rows_range, cols_range = RowCol.get_bounds(region)

        # Detect corners by investigation bocks of 2x2 items

        for row in range(rows_range[0], rows_range[1] + 2):
            for col in range(cols_range[0], cols_range[1] + 2):
                # "(row, col)" is about the top left corner of that tile
                loc = RowCol(row, col)
                square = [
                    loc + RowCol(-1, -1),
                    loc + RowCol(-1, 0),
                    loc + RowCol(0, -1),
                    loc,
                ]
                locs_in_square = [
                    square_loc for square_loc in square if square_loc in region
                ]
                count_in_square = len(locs_in_square)
                if count_in_square == 0 or count_in_square == 4:
                    pass  # No effect on corners
                elif count_in_square == 1 or count_in_square == 3:
                    corners += 1  # Inner / outer corner!
                else:
                    # If two items are diagonal:
                    if (
                        locs_in_square[0].row != locs_in_square[1].row
                        and locs_in_square[0].col != locs_in_square[1].col
                    ):
                        corners += 2  # We'll count this corner double
                    else:
                        pass  # Two blocks are in line and don't form a corner

        return area * corners


if __name__ == "__main__":
    main(Day12)
