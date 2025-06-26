from dataclasses import dataclass
from typing import List, Self, TypeVar

from bidict import bidict

from advent_of_code.shared import Direction

T = TypeVar("T")


@dataclass
class RowCol:
    """2-dimensional integer locinate, with basic arithmetics.

    Rows and column are 0 indexed and (0,0) should be the first tile in the top
    left corner.
    """

    row: int
    col: int

    def __iadd__(self, other: Self) -> Self:
        self.col += other.col
        self.row += other.row
        return self

    def __eq__(self, other: Self) -> bool:
        return self.col == other.col and self.row == other.row

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def copy(self) -> Self:
        return RowCol(row=self.row, col=self.col)

    def access(self, matrix: List[List[T]]) -> T:
        return matrix[self.row][self.row]

    def next(self, direction: Direction) -> Self:
        """Return a new location in a specified direction."""
        if direction == Direction.NORTH:
            return RowCol(self.col, self.row - 1)
        if direction == Direction.EAST:
            return RowCol(self.col + 1, self.row)
        if direction == Direction.SOUTH:
            return RowCol(self.col, self.row + 1)
        return RowCol(self.col - 1, self.row)


class GridItem:
    """Base class for an item in a grid.

    Typically, an item is represented by a single character, this can be passed in.
    """

    def __init__(self, loc: RowCol | None = None, character: str | None = None):
        """

        :param loc:   Coordinate of this item - for best result the same object must
                        be used as a key in the grid parent object!
        :param character:
        """
        self.character = character
        self.loc: RowCol | None = loc
        self.direction: Direction | None = None


class Grid:
    """Container for objects on a 2D grid (integer locinates).

    Squares on the grid may be empty.
    """

    def __init__(self):
        self.items: bidict[RowCol, GridItem] = bidict()
        # Contents of the grid - ``None`` by default

        # Grid size:
        self.rows: int = 0
        self.cols: int = 0

    def add_str_row(self, line: str, ignore: str = "."):
        """Add a row to this grid from a string.

        Each character will become a ``GridItem``.

        :param line:
        :param ignore: Consider this character as an empty tile
        """

        row = self.rows
        self.rows += 1

        for column, t in enumerate(line.strip()):
            if t == ignore:
                continue  # Do nothing

            loc = RowCol(col=column, row=row)
            item = GridItem(loc, t)
            self.cols = max(self.cols, column + 1)

            self.items[loc] = item

    def get_item_by_character(self, character: str) -> GridItem:
        """Return a single item or raise an exception."""
        item_found = None
        for item in self.items.values():
            if item.character == character:
                if item_found is not None:
                    raise KeyError(f"Item `{character}` is not unique")
                item_found = item

        if item_found is None:
            raise KeyError(f"Could not find item `{character}`")

        return item_found

    def remove(self, item: GridItem):
        self.items.inverse.pop(item)

    def in_range(self, loc: RowCol) -> bool:
        """Return true when a locinates falls in he grid range."""
        return 0 < loc.row < self.rows and 0 < loc.col < self.cols

    def find_next(self, loc: RowCol, direction: Direction) -> GridItem | None:
        """Find the next (if any) tile from a starting point into a direction."""
        next_loc = loc
        while self.in_range(next_loc):
            next_loc = next_loc.next(direction)
            if next_loc in self.items:
                return self.items[next_loc]

        return None
