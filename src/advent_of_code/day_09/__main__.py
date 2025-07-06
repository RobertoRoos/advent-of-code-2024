from dataclasses import dataclass
from typing import Self

from sortedcontainers import SortedList

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

    def __lt__(self, other: Self) -> bool:
        """Comparison operator."""
        return self.start < other.start


BlockList = SortedList[Block]


class Day09(Solver):

    def __call__(self) -> str:

        line = next(self.iterate_input())

        position = 0
        identification = 0
        full = True
        blocks: BlockList = SortedList()
        for c in line.strip():
            number = int(c)
            if not full:
                full = True
            else:
                block = Block(start=position, length=number, name=identification)
                blocks.add(block)
                identification += 1
                full = False

            position += number

        if self.args.part == 1:
            compacted_blocks = self.compact_blocks_by_byte(blocks)
        else:
            compacted_blocks = self.compact_blocks_whole(blocks)

        value = self.checksum(compacted_blocks)

        return str(value)

    @staticmethod
    def compact_blocks_by_byte(blocks: BlockList) -> BlockList:
        # Now to do the compacting:
        compacted_blocks: BlockList = SortedList()
        position = 0  # Byte position in the original blocks list

        while len(blocks) > 0:
            # Find the next gap in the original list:
            while len(blocks) > 1 and blocks[0].in_range(position):
                block = blocks.pop(0)
                compacted_blocks.add(block)
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

                compacted_blocks.add(block)
                position += block.length

        return compacted_blocks

    @staticmethod
    def compact_blocks_whole(blocks: BlockList) -> BlockList:

        tail_idx = len(blocks) - 1

        while tail_idx > 0:
            block_tail: Block = blocks[tail_idx]
            # Look for a better space for this block:
            moved = False
            for block_1, block_2 in zip(blocks[:-1], blocks[1:]):
                if block_2.start > block_tail.start:
                    break  # Already past the block in question

                gap_size = block_2.start - block_1.end
                if block_tail.length <= gap_size:
                    blocks.pop(tail_idx)
                    block_tail.start = block_1.end
                    blocks.add(block_tail)
                    moved = True
                    break

            if not moved:
                tail_idx -= 1  # Couldn't move this last item

        return blocks

    @staticmethod
    def checksum(blocks: BlockList) -> int:
        """Get weird checksum."""
        checksum = 0
        for block in blocks:
            for pos in range(block.start, block.end):
                checksum += pos * block.name
        return checksum

    @staticmethod
    def print_block(blocks: BlockList):
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
