from collections import defaultdict
from typing import Dict, List, Iterable, Tuple
from enum import StrEnum

from advent_of_code.shared import Direction, RowCol, Solver, main, PriorityList

Buttons = Dict[str, RowCol]


class KeypadType(StrEnum):
    """The different types of keypads we have."""
    NUMERIC = "numeric"
    DIRECTIONAL = "directional"


class Keypad:
    """Abstraction of a specific keypad."""

    # The layout of the buttons on a pad:
    BUTTONS: Dict[KeypadType, Buttons] = {
        KeypadType.NUMERIC: {
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
        },
        KeypadType.DIRECTIONAL: {
            "x": RowCol(0, 0),  # < Missing space
            "^": RowCol(0, 1),
            "A": RowCol(0, 2),
            "<": RowCol(1, 0),
            "v": RowCol(1, 1),
            ">": RowCol(1, 2),
        }
    }

    # Look-up table on how to navigate from any button to another button
    # (including the final 'A' to press that button):
    PATH_DIRECTIONS: Dict[KeypadType, Dict[Tuple[str, str], str]] = {}

    def __init__(self, pad_type: KeypadType, position: str = "A"):

        if not self.PATH_DIRECTIONS:
            Keypad.build_lookup()

        self.pad_type = pad_type
        self.loc: RowCol = RowCol(0, 0)
        self.position: str = ""
        self.move_to(position)

    def move_to(self, position: str):
        """Update internal location and button name."""
        self.loc = self.BUTTONS[self.pad_type][position]
        self.position = position

    def press_button_series(self, buttons: str) -> str:
        """Instantly process a sequence of buttons."""
        return "".join(
            self.press_button(b) for b in buttons
        )

    def press_button(self, target: str) -> str:
        """Find the directional keypad presses we'd need to press the target.

        This includes the 'activate' press at the end.
        A path is chosen to minimize switching buttons.

        Also update internal position
        """
        path = self.PATH_DIRECTIONS[self.pad_type][(self.position, target)]
        self.position = target
        return path

    @classmethod
    def build_lookup(cls):
        """Build the directional lookup table."""
        for pad_type in KeypadType:
            buttons = cls.BUTTONS[pad_type]

            cls.PATH_DIRECTIONS[pad_type] = {}

            for button_from in buttons.keys():
                for button_to in buttons.keys():
                    if button_to == "x" or button_from == "x":
                        continue

                    path = cls.find_keypad_directions(
                        pad_type, buttons[button_from], buttons[button_to]
                    )
                    path_str = "".join(
                        direction.to_symbol() for direction in path
                    ) + "A"

                    cls.PATH_DIRECTIONS[pad_type][(button_from, button_to)] = path_str

        # The preference for horizontal makes sure that the move from "A" to "<"
        # happens like "<v<A" (instead of "v<<A"), which is preferred according
        # to the sample.

        # But this will mess up some numeric directions, we'll just hard-code
        # correct them:

    @classmethod
    def find_keypad_directions(
            cls, pad_type: KeypadType, start: RowCol, target: RowCol
        ) -> Iterable[Direction]:
        """Find the steps needed to navigate to a button.

        Moving horizontally first is always preferred! This notion is mainly copied
        from the example, I am personally no sure why this is important.
        """
        loc = start.copy()

        while loc != target:
            found_next = False
            for next_direction in loc.directions_to(target, north_south_first=False):
                next_loc = loc.next(next_direction)
                if next_loc == cls.BUTTONS[pad_type]["x"]:
                    continue

                loc = next_loc
                found_next = True
                yield next_direction

            if not found_next:
                raise RuntimeError("Failed to find next keypad path")

    @classmethod
    def consecutive_keypads(cls, pads: List["Keypad"], sequence: str) -> Iterable[str]:
        """Go through a stack of keypads in one go.

        Relies on recursion.
        """
        next_sequence = pads[0].press_button_series(sequence)
        yield next_sequence

        if len(pads) > 1:
            yield from cls.consecutive_keypads(pads[1:], next_sequence)


class Day21(Solver):

    def __call__(self) -> str:
        return ""
    #     codes: List[str] = [txt.strip() for txt in self.iterate_input()]
    #
    #     keypads = [
    #         Keypad(self.KEYPAD_NUMERIC),
    #         Keypad(self.KEYPAD_DIRECTIONAL),
    #         Keypad(self.KEYPAD_DIRECTIONAL),
    #     ]
    #     # The relevant keypads and their positions
    #
    #     score = 0
    #
    #     for code in codes:
    #         button_presses = [code]
    #         for keypad in keypads:
    #             next_keypad_buttons = ""
    #             for c in button_presses[-1]:
    #                 next_keypad_buttons += keypad.find_and_press_button(c)
    #
    #             if keypad.position != "A":
    #                 raise RuntimeError("Keypad hasn't returned to A position!")
    #
    #             button_presses.append(next_keypad_buttons)
    #
    #         complexity = len(button_presses[-1])
    #         code_int = int(code[:-1])
    #         score += complexity * code_int
    #
    #     return str(score)
    #
    # def find_best_direction_buttons(
    #         self, pads: List[Keypad], first_buttons: str
    # ) -> str:
    #     buttons: List[str] = [""] * len(pads)
    #
    #     # for button in first_buttons:
    #     #     paths: List[List[str]] = []
    #     #     for i, this_pad in enumerate(pads):
    #     #         for this_path in this_pad.find_all_keypad_directions(button):
    #
    #     # target_button = first_buttons[0]
    #     # new_paths = []
    #     # for i, _ in enumerate(pads):
    #     #     paths = list(
    #     #         pads[i].find_all_keypad_directions(target_button)
    #     #     )
    #     #     all_paths.append(paths)
    #
    #     # target_button = first_buttons[0]
    #     #
    #     # all_paths = defaultdict(dict)
    #     # collection = all_paths
    #     # for i, this_pad in enumerate(pads):
    #     #     for this_path in this_pad.find_all_keypad_directions(target_button):
    #     #         collection[this_pad]
    #
    #     return buttons_dir


if __name__ == "__main__":
    main(Day21)
