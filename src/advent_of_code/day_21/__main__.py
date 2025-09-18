from typing import Dict, List

from advent_of_code.shared import Direction, RowCol, Solver, main

Buttons = Dict[str, RowCol]


class Keypad:
    """Abstraction of a specific keypad."""

    def __init__(self, buttons: Buttons, position: str = "A"):
        self.buttons: Buttons = buttons
        self.loc: RowCol = RowCol(0, 0)
        self.move_to(position)

    def move_to(self, position: str):
        self.loc = self.buttons[position]

    def find_directional_keypad_presses(self, target: str) -> str:
        """Find the directional keypad presses we'd need to press the target.

        This includes the 'activate' press at the end.
        A path is chosen to minimize switching buttons.
        """
        target_loc = self.buttons[target]

        buttons = ""
        for direction in self.find_keypad_directions(target_loc):
            buttons += direction.to_symbol()

        buttons += "A"
        return buttons

    def find_keypad_directions(self, target: RowCol) -> List[Direction]:
        """Basic path finding across the keypad."""
        for north_south_first in [True, False]:
            loc = self.loc
            directions = []
            while loc != target:
                direction = self.get_direction_from_diff(
                    target - loc,
                    north_south_first,
                )
                next_loc = loc.next(direction)
                if next_loc == self.buttons["x"]:
                    directions = None
                    break

                directions.append(direction)
                loc = next_loc

            if directions is not None:
                return directions

        raise RuntimeError("Failed to navigate keypad")

    @staticmethod
    def get_direction_from_diff(
        diff: RowCol, north_south_first: bool = True
    ) -> Direction:
        """Reduce a difference in location to a direction."""
        if diff.row > 0 and (north_south_first or diff.col == 0):
            return Direction.SOUTH
        elif diff.row < 0 and (north_south_first or diff.col == 0):
            return Direction.NORTH
        elif diff.col > 0:
            return Direction.EAST
        elif diff.col < 0:
            return Direction.WEST
        else:
            raise ValueError(f"Cannot get a direction from `{diff}`")


class Day21(Solver):

    KEYPAD_NUMERIC: Buttons = {
        "7": RowCol(0, 0),
        "8": RowCol(0, 1),
        "9": RowCol(0, 2),
        "4": RowCol(1, 0),
        "5": RowCol(1, 1),
        "6": RowCol(1, 2),
        "1": RowCol(2, 0),
        "2": RowCol(2, 1),
        "3": RowCol(2, 2),
        "x": RowCol(3, 0),  # < Missing space
        "0": RowCol(3, 1),
        "A": RowCol(3, 2),
    }

    KEYPAD_DIRECTIONAL: Buttons = {
        "x": RowCol(0, 0),  # < Missing space
        "^": RowCol(0, 1),
        "A": RowCol(0, 2),
        "<": RowCol(1, 0),
        "v": RowCol(1, 1),
        ">": RowCol(1, 2),
    }

    def __call__(self) -> str:
        codes: List[str] = [txt.strip() for txt in self.iterate_input()]

        keypads = [
            Keypad(self.KEYPAD_NUMERIC),
            Keypad(self.KEYPAD_DIRECTIONAL),
            Keypad(self.KEYPAD_DIRECTIONAL),
        ]
        # The relevant keypads and their positions

        score = 0

        for code in codes:
            button_presses = [code]
            for keypad in keypads:
                next_keypad_buttons = ""
                for c in button_presses[-1]:
                    next_keypad_buttons += keypad.find_directional_keypad_presses(c)
                    keypad.move_to(c)

                button_presses.append(next_keypad_buttons)

            complexity = len(button_presses[-1])
            code_int = int(code[:-1])
            score += complexity * code_int

        return str(score)


if __name__ == "__main__":
    main(Day21)
