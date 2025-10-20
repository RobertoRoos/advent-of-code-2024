from typing import List, Self

from advent_of_code.shared import Solver, main


class Tumblers:
    """Abstraction for either a lock or a key."""

    def __init__(self, block: List[str]):
        self.size = len(block)  # Numer of possible positions
        self.positions = [0 for _ in block[0]]

        for line in block:
            for j, char in enumerate(line):
                if char == "#":
                    self.positions[j] += 1

    def fit_key(self, key: Self) -> bool:
        """Return `True` if this lock could fit that key."""
        for lock_pos, key_pos in zip(self.positions, key.positions):
            if self.size - lock_pos < key_pos:
                return False  # Not enough space

        return True


class Day25(Solver):

    def __call__(self) -> str:

        # Parse inputs:

        locks: List[Tumblers] = []
        keys: List[Tumblers] = []

        is_lock = None
        lines_block: List[str] = []

        for line in self.get_input():
            line = line.strip()  # To get the last empty line, avoid `iterate_input`

            if is_lock is None:
                is_lock = line[0] == "#"
                continue

            if not line:
                new_object = Tumblers(lines_block)
                this_list = locks if is_lock else keys
                this_list.append(new_object)

                is_lock = None
                lines_block = []
                continue

            if is_lock:
                lines_block.append(line)
            else:
                lines_block.insert(0, line)

        # Compare:
        result = 0
        for lock in locks:
            for key in keys:
                if lock.fit_key(key):
                    result += 1

        return str(result)


if __name__ == "__main__":
    main(Day25)
