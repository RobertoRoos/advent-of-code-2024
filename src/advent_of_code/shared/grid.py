from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Self, Set, Tuple, TypeVar

from bidict import bidict

from .coordinates import Direction
from .priority_list import PriorityList

T = TypeVar("T")


@dataclass
class RowCol:
    """2-dimensional integer location, with basic arithmetics.

    Rows and column are 0 indexed and (0,0) should be the first tile in the top
    left corner.
    """

    row: int
    col: int

    def __add__(self, other: Self) -> Self:
        return RowCol(row=self.row + other.row, col=self.col + other.col)

    def __sub__(self, other: Self) -> Self:
        return RowCol(row=self.row - other.row, col=self.col - other.col)

    def __mul__(self, other: int) -> Self:
        return RowCol(row=self.row * other, col=self.col * other)

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

    def tuple(self) -> Tuple[int, int]:
        return self.row, self.col

    def next(self, direction: Direction) -> Self:
        """Return a new location in a specified direction."""
        if direction == Direction.NORTH:
            return RowCol(self.row - 1, self.col)
        if direction == Direction.EAST:
            return RowCol(self.row, self.col + 1)
        if direction == Direction.SOUTH:
            return RowCol(self.row + 1, self.col)
        if direction == Direction.WEST:
            return RowCol(self.row, self.col - 1)
        raise ValueError(f"Unrecognized direction `{direction}`")

    def neighbours(self) -> Iterable[Self]:
        """Yield the neighbours of this location."""
        yield RowCol(row=self.row + 1, col=self.col)
        yield RowCol(row=self.row, col=self.col + 1)
        yield RowCol(row=self.row - 1, col=self.col)
        yield RowCol(row=self.row, col=self.col - 1)

    @staticmethod
    def get_bounds(
        items: Iterable["RowCol"],
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get outer bounds of a set of items."""
        rows_range_min, rows_range_max = None, None
        cols_range_min, cols_range_max = None, None

        # Determine bounds:
        for loc in items:
            if rows_range_min is None or loc.row < rows_range_min:
                rows_range_min = loc.row
            if rows_range_max is None or loc.row > rows_range_max:
                rows_range_max = loc.row
            if cols_range_min is None or loc.col < cols_range_min:
                cols_range_min = loc.col
            if cols_range_max is None or loc.col > cols_range_max:
                cols_range_max = loc.col

        return (rows_range_min, rows_range_max), (cols_range_min, cols_range_max)

    @staticmethod
    def from_str(text: str) -> "RowCol":
        """Turn a string like `5,1` into a row-col object."""
        values = text.split(",")
        if len(values) != 2:
            raise ValueError(f"Text {text} does not contain two coordinates")

        values = [int(v) for v in values]

        return RowCol(row=values[0], col=values[1])

    @staticmethod
    def from_direction(direction: Direction) -> "RowCol":
        """Create a difference RowCol based on a direction."""
        if direction == Direction.NORTH:
            return RowCol(row=-1, col=0)
        if direction == Direction.EAST:
            return RowCol(row=0, col=1)
        if direction == Direction.SOUTH:
            return RowCol(row=1, col=0)
        if direction == Direction.WEST:
            return RowCol(row=0, col=-1)
        raise ValueError(f"Unrecognized direction `{direction}`")

    def transpose(self) -> Self:
        """Get version with row / column flipped."""
        return RowCol(row=self.col, col=self.row)

    def distance(self, other: Self) -> int:
        """Get number of horizontal/vertical steps between two points."""
        return abs(self.row - other.row) + abs(self.col - other.col)


Path = List[RowCol]


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
        self.data: Dict[Any, Any] = {}

    def __repr__(self) -> str:
        return f"GridItem('{self.character}', row={self.loc.row}, col={self.loc.col})"


class Grid:
    """Container for objects on a 2D grid (integer locations).

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
        The full string will determine the bounds of the grid, even for
        ignore tiles.

        :param line:
        :param ignore: Consider this character as an empty tile
        """

        row = self.rows
        self.rows += 1

        line = line.strip()
        if self.cols is None or self.cols == 0:
            self.cols = len(line)
        elif self.cols != len(line):
            raise ValueError(f"Unexpected line length {len(line)} for {self.cols} cols")

        for column, t in enumerate(line.strip()):
            if t == ignore:
                continue  # Do nothing

            loc = RowCol(col=column, row=row)
            item = GridItem(loc, t)

            self.items[loc] = item

    def copy(self) -> Self:
        new_grid = Grid()
        new_grid.cols = self.cols
        new_grid.rows = self.rows
        new_grid.items = self.items.copy()
        return new_grid

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

    def add(self, item: GridItem):
        self.items[item.loc] = item

    def remove(self, item: GridItem):
        self.items.inverse.pop(item)

    def remove_location(self, loc: RowCol):
        self.items.pop(loc)

    def in_range(self, loc: RowCol) -> bool:
        """Return true when a locations falls in he grid range."""
        return 0 <= loc.row < self.rows and 0 <= loc.col < self.cols

    def find_next(self, loc: RowCol, direction: Direction) -> GridItem | None:
        """Find the next (if any) tile from a starting point into a direction."""
        next_loc = loc
        while self.in_range(next_loc):
            next_loc = next_loc.next(direction)
            if next_loc in self.items:
                return self.items[next_loc]

        return None

    def neighbours(self, tile: GridItem) -> Iterable[GridItem]:
        """Loop over the neighbouring tiles, where they exist."""
        for next_loc in tile.loc.neighbours():
            if next_loc in self.items:
                yield self.items[next_loc]

    def find_region(
        self, tile: GridItem, region: None | Dict[RowCol, GridItem] = None
    ) -> Dict[RowCol, GridItem]:
        """Return list of all recursive neighbours with the same character.

        :return: Dict like {"loc": "item"}
        """
        if region is None:
            region = {}

        region[tile.loc] = tile

        for neighbour in self.neighbours(tile):
            if neighbour.character == tile.character:
                if neighbour.loc in region:
                    continue  # This neighbour is already considered in the region,
                    # prevent duplicate

                region = self.find_region(neighbour, region)

        return region

    def find_path(
        self, start: RowCol, goal: RowCol, wall_characters: Set[str] | None = None
    ) -> Tuple[int, Path]:
        """Find a path through the grid from start goal to some end.

        A lot of puzzles have some kind of maze solving, so we write this in the shared
        code.
        This using Dijkstras algorithm directly.

        :return: The length of the shortest path and the path itself
        """
        if wall_characters is None:
            wall_characters = set("#")

        path_queue = PriorityList[Path]()
        shortest_distances: Dict[RowCol, int] = {}

        path_queue.push(0, [start])

        while path_queue:
            this_distance, this_path = path_queue.pop()
            this_loc = this_path[-1]

            if this_loc == goal:
                return this_distance, this_path

            # Find next options:
            for direction in Direction:
                next_loc = this_loc.next(direction)
                if not self.in_range(next_loc):
                    continue  # Cannot go this way
                if next_loc in self.items:
                    if self.items[next_loc].character in wall_characters:
                        continue  # Blocked

                next_distance = this_distance + 1
                if (
                    next_loc not in shortest_distances
                    or next_distance < shortest_distances[next_loc]
                ):
                    # Found a better path!
                    shortest_distances[next_loc] = next_distance
                    path_queue.push(next_distance, this_path[:] + [next_loc])

        raise RuntimeError("Failed to find path")

    def print_path(self, path: Path, char: str = "o"):
        """Print a path into this grid.

        Any existing tiles might get overwritten!
        """
        path_grid = self.copy()
        for step in path:
            item = GridItem(loc=step, character=char)
            path_grid.add(item)

        path_grid.print()

    def print(self, data_key: None | str = None, end: str = "", padding: int = 0):
        print()
        for row in range(self.rows):
            for col in range(self.cols):
                loc = RowCol(row=row, col=col)
                item = self.items.get(loc, None)
                if item is None:
                    txt = "."
                elif data_key is None:
                    txt = item.character
                else:
                    txt = item.data[data_key]
                txt = str(txt)
                if padding > 0 and len(txt) < padding:
                    str_pad = "".join([" "] * (padding - len(txt)))
                    txt = str_pad + txt
                print(txt, end=end)
            print()
        print()
