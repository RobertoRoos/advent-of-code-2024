from bidict import bidict

from advent_of_code.shared import Coord2D, Direction


class GridItem:
    """Base class for an item in a grid.

    Typically, an item is represented by a single character, this can be passed in.
    """

    def __init__(self, coord: Coord2D | None = None, character: str | None = None):
        """

        :param coord:   Coordinate of this item - for best result the same object must
                        be used as a key in the grid parent object!
        :param character:
        """
        self.character = character
        self.coord: Coord2D | None = coord
        self.direction: Direction | None = None


class Grid:
    """Container for objects on a 2D grid (integer coordinates).

    Squares on the grid may be empty.
    """

    def __init__(self):
        self.items: bidict[Coord2D, GridItem] = bidict()
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

            coord = Coord2D(x=column, y=row)
            item = GridItem(coord, t)
            self.cols = max(self.cols, column + 1)

            self.items[coord] = item

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

    def in_range(self, coord: Coord2D) -> bool:
        """Return true when a coordinates falls in he grid range."""
        return 0 < coord.row < self.rows and 0 < coord.col < self.cols

    def find_next(self, coord: Coord2D, direction: Direction) -> GridItem | None:
        """Find the next (if any) tile from a starting point into a direction."""
        next_coord = coord
        while self.in_range(next_coord):
            next_coord = next_coord.next(direction)
            if next_coord in self.items:
                return self.items[next_coord]

        return None
