from enum import StrEnum
from typing import Dict, List, Tuple

from advent_of_code.shared import Direction, RowCol, Solver, main

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
        },
    }

    # Look-up table on how to possibly navigate from any button to another button
    # (including the final 'A' to press that button):
    PATH_DIRECTIONS: Dict[KeypadType, Dict[Tuple[str, str], List[str]]] = {}

    MIN_COMPLEXITY_CACHE: Dict[Tuple[int, str], int] = {}

    def __init__(self, pad_type: KeypadType):

        if not self.PATH_DIRECTIONS:
            Keypad.build_lookup()

        self.pad_type = pad_type

    def get_button_paths(self, start: str, target: str) -> List[str]:
        """Get possible paths to go from one button to another."""
        return self.PATH_DIRECTIONS[self.pad_type][(start, target)]

    def get_sequence_paths(self, code: str) -> List[List[str]]:
        """List all the possible paths per character in the code.

        Assume we start hovering over "A".
        """
        sequences = []
        prev = "A"
        for char in code:
            sequences.append(self.get_button_paths(prev, char))
            prev = char

        return sequences

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

                    paths = cls.find_all_keypad_directions(
                        pad_type, buttons[button_from], buttons[button_to]
                    )
                    path_strs = [
                        "".join(direction.to_symbol() for direction in path) + "A"
                        for path in paths
                    ]

                    cls.PATH_DIRECTIONS[pad_type][(button_from, button_to)] = path_strs

    @classmethod
    def find_all_keypad_directions(
        cls, pad_type: KeypadType, start: RowCol, target: RowCol
    ) -> List[List[Direction]]:
        """Return a list of possible paths to a target across the keypad.

        The returned options are not weighted or sorted.
        """
        path_queue = [(start, [])]
        paths = []
        while path_queue:
            this_loc, this_path = path_queue.pop(0)

            if this_loc == target:
                paths.append(this_path)

            for direction in this_loc.directions_to(target):
                next_loc = this_loc.next(direction)
                if next_loc == cls.BUTTONS[pad_type]["x"]:
                    continue  # Dead end

                path_queue.append((next_loc, this_path[:] + [direction]))

        return paths

    @classmethod
    def get_final_complexity_of_stack(cls, pads: List["Keypad"], code: str) -> int:
        """Return the smallest directional sequence length of the stack of keypads.

        It finds the length of the shortest paths for chained pads.
        It works recursively and per individual button move.

        An important realization is that you cannot maintain a single strategy for
        button paths. Hence we rely on the various paths we built up once and keep
        trying. The recursion depth is limited by going character by character: the
        total number of complete sequences is huge for longer codes, but letter by
        letter it's minimal and those sub-sequences can be optimized independently.

        At a depth of 25 this bogs down - but there is loads of repetition. Each code
        (at a specified depth) will always have same min. complexity, so cache it to
        minimize recursion steps.
        """
        depth = len(pads) - 1
        cache_key = (depth, code)
        try:
            return cls.MIN_COMPLEXITY_CACHE[cache_key]
        except KeyError:
            pass

        paths_per_character = pads[0].get_sequence_paths(code)
        # Like: `[ <paths for char 1>, <paths for char 2>, ... ]``
        # List of lists of options for paths

        min_length = 0
        for paths in paths_per_character:
            if depth == 0:  # End of recursion depth
                min_length += min(map(len, paths))
            else:  # Recurse deeper
                min_length += min(
                    cls.get_final_complexity_of_stack(pads[1:], path) for path in paths
                )
            # Sum the length of the shortest string in each list

        cls.MIN_COMPLEXITY_CACHE[cache_key] = min_length

        return min_length


class Day21(Solver):

    def __call__(self) -> str:
        codes: List[str] = [txt.strip() for txt in self.iterate_input()]

        score = 0

        pads = [
            Keypad(KeypadType.NUMERIC),
        ]  # The relevant keypads (no position need to be tracked)

        depth = 2 if self.args.part == 1 else 25

        pads += [Keypad(KeypadType.DIRECTIONAL) for _ in range(depth)]

        for code in codes:
            complexity = Keypad.get_final_complexity_of_stack(pads, code)
            code_int = int(code[:-1])
            score += complexity * code_int

        return str(score)


if __name__ == "__main__":
    main(Day21)
