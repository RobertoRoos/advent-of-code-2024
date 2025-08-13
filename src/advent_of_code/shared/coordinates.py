from enum import StrEnum
from typing import Iterable, Self


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

    def opposite(self) -> Self:
        """Get the mirrored direction."""
        if self.value == self.NORTH.value:
            return Direction.SOUTH
        elif self.value == self.EAST.value:
            return Direction.WEST
        elif self.value == self.SOUTH.value:
            return Direction.NORTH
        else:
            return Direction.EAST

    def next_options(
        self, clockwise: bool = True, backwards: bool = True
    ) -> Iterable[Self]:
        """Yield possible follow-up directions.

        :param clockwise: See :meth:`rotate`
        :param backwards: If False (default), do not allow backing up
        """
        starting_direction = Direction(self.value)
        from_direction = starting_direction.opposite()
        next_direction = starting_direction

        while True:
            yield next_direction
            next_direction = next_direction.rotate(clockwise)
            if not backwards and next_direction == from_direction:
                next_direction = next_direction.rotate(clockwise)  # Rotate past it

            if next_direction == starting_direction:
                break

    def turns(self, other: Self, go_negative: bool = False) -> int:
        """Return number of turns (0, 1, 2 or 3) between this direction and the other.

        Counting clockwise. E.g. ``Direction.EAST.turns(Direction.SOUTH)`` will return
        ``1``.
        """
        this = Direction(self)
        turns = 0
        while this != other:
            this = this.rotate(clockwise=True)
            turns += 1

        if not go_negative:
            return turns

        return -1 if turns == 3 else turns
