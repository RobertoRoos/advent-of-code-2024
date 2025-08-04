from typing import List

from advent_of_code.shared import Direction, Grid, GridItem, RowCol, Solver, main


class Day15(Solver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = Grid()

    def __call__(self) -> str:

        doing_map = True

        instructions: List[Direction] = []

        for line in self.iterate_input():

            if line.strip() == "":
                doing_map = False
                continue

            if doing_map:
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
            if item.character != "O":
                continue

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
        target = self.robot  # The thing to move next
        diff = RowCol.from_direction(direction)
        to_be_moved: List[GridItem] = []  # List of items that are in the line
        while target is not None:
            next_loc = target.loc + diff
            next_target = self.grid.items.get(next_loc, None)
            if next_target is not None and next_target.character == "#":
                to_be_moved = []
                break  # There's a wall connected, move nothing

            to_be_moved.append(target)
            target = next_target

        # To prevent overlap we'll need to pop them each first:
        for item in to_be_moved:
            self.grid.remove(item)
        for item in to_be_moved:
            item.loc += diff
            self.grid.add(item)


if __name__ == "__main__":
    main(Day15)
