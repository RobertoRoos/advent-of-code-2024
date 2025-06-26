from dataclasses import dataclass
from enum import StrEnum
from typing import List, Self, TypeVar

T = TypeVar("T")


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


@dataclass
class Coord2D:
    """2-dimensional integer coordinate, with basic arithmetics."""

    x: int
    y: int

    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        return self

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @property
    def row(self) -> int:
        return self.y

    @row.setter
    def row(self, value: int):
        self.y = value

    @property
    def col(self) -> int:
        return self.x

    @col.setter
    def col(self, value: int):
        self.x = value

    def copy(self) -> Self:
        return Coord2D(x=self.x, y=self.y)

    def access(self, matrix: List[List[T]]) -> T:
        return matrix[self.row][self.row]

    def next(self, direction: Direction) -> Self:
        """Return a new coordinate in a specified direction."""
        if direction == Direction.NORTH:
            return Coord2D(self.x, self.y - 1)
        if direction == Direction.EAST:
            return Coord2D(self.x + 1, self.y)
        if direction == Direction.SOUTH:
            return Coord2D(self.x, self.y + 1)
        return Coord2D(self.x - 1, self.y)
