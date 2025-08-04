from typing import List, Set

from advent_of_code.shared import Direction, Grid, GridItem, RowCol, Solver, main


class Day15(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = Grid()
        self.robot: GridItem | None = None

    def __call__(self) -> str:

        doing_map = True

        instructions: List[Direction] = []

        for line in self.iterate_input():

            line = line.strip()

            if line == "":
                doing_map = False
                continue

            if doing_map:
                if self.args.part == 2:
                    line = "".join(
                        [
                            "@." if c == "@" else "[]" if c == "O" else (c + c)
                            for c in line
                        ]
                    )
                self.grid.add_str_row(line)
            else:
                for char in line.strip():
                    instructions.append(self.direction_from_char(char))

        self.robot = self.grid.get_item_by_character("@")

        # Perform all instructions:
        for instruction in instructions:
            self.move_robot(instruction)

        # Compute score now:
        score = 0
        for item in self.grid.items.values():
            if item.character == "O" or item.character == "[":
                score += 100 * item.loc.row + item.loc.col

        return str(score)

    @staticmethod
    def direction_from_char(char: str) -> Direction:
        if char == ">":
            return Direction.EAST
        if char == "^":
            return Direction.NORTH
        if char == "<":
            return Direction.WEST
        if char == "v":
            return Direction.SOUTH

        raise ValueError(f"Unrecognized direction `{char}`")

    def move_robot(self, direction: Direction):
        """Move the robot in a direction (in the grid property)."""
        to_be_moved = self.find_item_chain(self.robot, direction)

        if to_be_moved is None:
            return

        diff = RowCol.from_direction(direction)

        # To prevent overlap we'll need to pop them each first:
        for item in to_be_moved:
            self.grid.remove(item)
        for item in to_be_moved:
            item.loc += diff
            self.grid.add(item)

    def find_item_chain(
        self, item: GridItem, direction: Direction
    ) -> Set[GridItem] | None:
        """Return a chain of items that would move together.

        Or return ``None`` if a wall would be hit, making movement impossible.

        The item itself is included.
        """
        diff = RowCol.from_direction(direction)
        next_loc = item.loc + diff
        next_item = self.grid.items.get(next_loc, None)

        recursing_items = []

        if next_item is not None:
            next_item_char = next_item.character
            if next_item_char == "#":
                return None

            if next_item_char == "O" or next_item_char == "[" or next_item_char == "]":
                recursing_items.append(next_item)
                if (next_item_char == "[" or next_item_char == "]") and (
                    direction == Direction.NORTH or direction == Direction.SOUTH
                ):
                    other_next_item_loc = next_item.loc + RowCol(
                        row=0, col=(1 if next_item_char == "[" else -1)
                    )
                    other_next_item = self.grid.items[other_next_item_loc]
                    recursing_items.append(other_next_item)
            else:
                raise RuntimeError(f"Unrecognized neighbour `{next_item_char}`")

        return_items = {item}
        # Not very neat, but when two wide blocks are above each other we need to
        # prevents the upper block being added twice
        for recursing_item in recursing_items:
            sub_items = self.find_item_chain(recursing_item, direction)
            if sub_items is None:
                return None  # Hit a wall! Cancel everything

            return_items = return_items.union(sub_items)

        return return_items


if __name__ == "__main__":
    main(Day15)
