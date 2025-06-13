from dataclasses import dataclass
from typing import List, Self, TypeVar

T = TypeVar("T")


@dataclass
class Coord2D:
    """2-dimensional integer coordinate, with basic arithmetics."""

    x: int
    y: int

    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        return self

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
