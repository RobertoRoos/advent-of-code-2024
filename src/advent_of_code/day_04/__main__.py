import re

from advent_of_code.shared import Coord2D, Solver, main


class Day04(Solver):

    def __call__(self) -> str:
        lines = self.get_input()

        if lines[-1] == "":
            lines.pop(-1)

        rows = len(lines)
        cols = len(lines[0])

        # Horizontal, normal
        lines_set = lines[:]

        # Horizontal, reversed
        lines_set += ["".join(reversed(t)) for t in lines]

        # Vertical, normal
        lines_vert = []
        for col in range(cols):
            line = ""
            for row in range(rows):
                line += lines[row][col]
            lines_vert.append(line)
        lines_set += lines_vert

        # Vertical, reversed
        lines_set += ["".join(reversed(t)) for t in lines_vert]

        # Diagonal right, normal
        lines_diag_right = []
        corner = Coord2D(
            x=cols - 1, y=0
        )  # Coordinate of the left-upper corner of the diagonal
        while corner.row < rows:
            idx = corner.copy()
            line = ""
            while 0 <= idx.row < rows and 0 <= idx.col < cols:
                line += lines[idx.row][idx.col]
                idx += Coord2D(1, 1)
            if corner.col > 0:
                corner.col -= 1
            else:
                corner.row += 1

            lines_diag_right.append(line)

        lines_set += lines_diag_right

        # Diagonal right, reversed
        lines_set += ["".join(reversed(t)) for t in lines_diag_right]

        # Diagonal left, normal
        lines_diag_left = []
        corner = Coord2D(
            x=0, y=0
        )  # Coordinate of the left-lower corner of the diagonal
        while corner.col < cols:
            idx = corner.copy()
            line = ""
            while 0 <= idx.row < rows and 0 <= idx.col < cols:
                line += lines[idx.row][idx.col]
                idx += Coord2D(1, -1)
            if corner.row < rows - 1:
                corner.row += 1
            else:
                corner.col += 1

            lines_diag_left.append(line)

        lines_set += lines_diag_left

        # Diagonal left, reversed
        lines_set += ["".join(reversed(t)) for t in lines_diag_left]

        re_word = re.compile(r"XMAS")
        lines_all = "\n".join(lines_set)
        matches = re_word.findall(lines_all)
        return str(len(matches))


if __name__ == "__main__":
    main(Day04)
