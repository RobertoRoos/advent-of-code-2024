from dataclasses import dataclass
from typing import List, Self

from advent_of_code.shared import Solver, main


@dataclass
class Block:
    """Abstraction for a data block."""

    start: int  # First byte in this block (0-indexed)
    length: int  # Number of bytes in this block
    name: int  # Block-ID

    @property
    def end(self) -> int:
        """Final index, *after* this block (so exclusive)."""
        return self.start + self.length

    def in_range(self, pos: int) -> bool:
        """Check if this position fall in this block."""
        return self.start <= pos < self.end

    def copy(self) -> Self:
        return Block(start=self.start, length=self.length, name=self.name)


class Day09(Solver):

    def __call__(self) -> str:

        line = next(self.iterate_input())

        position = 0
        identification = 0
        full = True
        blocks: List[Block] = []
        for c in line.strip():
            number = int(c)
            if not full:
                full = True
            else:
                block = Block(start=position, length=number, name=identification)
                blocks.append(block)
                identification += 1
                full = False

            position += number

        # self.print_block(blocks)

        # Now to do the compacting:
        compacted_blocks: List[Block] = []
        position = 0  # Byte position in the original blocks list

        while len(blocks) > 0:
            # Find the next gap in the original list:
            while len(blocks) > 1 and blocks[0].in_range(position):
                block = blocks.pop(0)
                compacted_blocks.append(block)
                position += block.length

            # Keep filling this gap:
            while len(blocks) > 0 and (gap_size := blocks[0].start - position) > 0:
                if len(blocks) == 1:
                    gap_size = 999999  # Actually there is loads of space now

                if gap_size >= blocks[-1].length:
                    # Move the entire block
                    block = blocks.pop(-1)
                    block.start = position
                else:
                    old_block = blocks[-1]
                    block = Block(start=position, length=gap_size, name=old_block.name)
                    old_block.length -= gap_size

                compacted_blocks.append(block)
                position += block.length

            # self.print_block(compacted_blocks)

        value = self.checksum(compacted_blocks)

        return str(value)

    @staticmethod
    def checksum(blocks: List[Block]) -> int:
        """Get weird checksum."""
        checksum = 0
        for block in blocks:
            for pos in range(block.start, block.end):
                checksum += pos * block.name
        return checksum

    @staticmethod
    def print_block(blocks: List[Block]):
        position = 0
        block_idx = 0
        print()
        while position < blocks[-1].end:
            if blocks[block_idx].in_range(position):
                c = blocks[block_idx].name
            else:
                c = "."

            print(c, end="")
            position += 1
            if position >= blocks[block_idx].end:
                block_idx += 1
        print()


if __name__ == "__main__":
    main(Day09)
