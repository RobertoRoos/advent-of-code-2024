import re
from dataclasses import dataclass
from typing import List, Tuple

from advent_of_code.shared import Solver, main

XY = Tuple[int, int]


@dataclass
class Game:
    """Helper object for a single claw machine."""

    COST_A: int = 3
    COST_B: int = 1

    def __init__(self, *args, **kwargs):
        self.button_a: XY = (0, 0)
        self.button_b: XY = (0, 0)
        self.prize: XY = (0, 0)

        if args or kwargs:
            super().__init__(*args, **kwargs)

    def get_button_presses(self) -> None | Tuple[int, int]:
        """Return the minimum number of button presses to win this game.

        We really solve the question by composing a 2x2 matrix for the two equations,
        one for X and one for Y.
        """
        det = self.button_a[0] * self.button_b[1] - self.button_a[1] * self.button_b[0]

        if det == 0:
            return None  # Not invertible

        # 2x2 matrix inverse:
        det_inv = 1.0 / det
        a = (
            self.prize[0] * det_inv * self.button_b[1]
            - self.prize[1] * det_inv * self.button_b[0]
        )
        b = (
            -self.prize[0] * det_inv * self.button_a[1]
            + self.prize[1] * det_inv * self.button_a[0]
        )

        a_int = int(round(a))
        b_int = int(round(b))

        if max(abs(b - b_int), abs(a - a_int)) > 0.001:
            # raise ValueError(f"Failed to find integer solution!")
            return None

        return a_int, b_int


class Day13(Solver):

    RE_INPUT = re.compile(r"(.+): X.(\d+), Y.(\d+)")

    def __call__(self) -> str:

        games: List[Game] = []

        new_game = None
        for line in self.iterate_input():
            line = line.strip()
            if not line:
                new_game = None
                continue

            if new_game is None:
                new_game = Game()

            match = self.RE_INPUT.match(line)
            xy = (int(match.group(2)), int(match.group(3)))
            name = match.group(1)
            if name == "Button A":
                new_game.button_a = xy
            elif name == "Button B":
                new_game.button_b = xy
            elif name == "Prize":
                if self.args.part == 2:
                    xy = (xy[0] + 10000000000000, xy[1] + 10000000000000)
                new_game.prize = xy
                games.append(new_game)
            else:
                raise ValueError(f"Didn't recognize `{name}`")

        score = 0
        for game in games:
            presses = game.get_button_presses()
            if presses is not None:
                this_score = presses[0] * Game.COST_A + presses[1] * Game.COST_B
                score += this_score

        return str(score)


if __name__ == "__main__":
    main(Day13)
