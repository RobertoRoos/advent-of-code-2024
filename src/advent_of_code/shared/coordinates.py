from enum import StrEnum
from typing import Self


class Direction(StrEnum):
    """One of four directions."""

    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

    def rotate(self, clockwise: bool = True) -> Self:
        """Return a new rotated direction."""
        if clockwise:
            if self.value == self.NORTH.value:
                return Direction.EAST
            elif self.value == self.EAST.value:
                return Direction.SOUTH
            elif self.value == self.SOUTH.value:
                return Direction.WEST
            else:
                return Direction.NORTH
        else:
            if self.value == self.NORTH.value:
                return Direction.WEST
            if self.value == self.EAST.value:
                return Direction.NORTH
            if self.value == self.SOUTH.value:
                return Direction.EAST
            else:
                return Direction.SOUTH
