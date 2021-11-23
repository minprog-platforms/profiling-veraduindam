from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid = [[int(i) for i in row] for row in puzzle]

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        block_index = (y // 3) * 3 + x // 3

        all_forbidden = set(self.row_values(y)).union(set(self.column_values(x)), set(self.block_values(block_index)))

        return options - all_forbidden

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            if 0 in set(self._grid[y]):
                x = self._grid[y].index(0)
                return x, y

        return -1, -1

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return self._grid[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return [row[i] for row in self._grid]

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values: list[int] = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for i in range(3):
            values = values + self._grid[y_start + i][x_start:x_start + 3]
        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        result = True

        for i in range(9):
            if set(self.row_values(i)) != values or set(self.row_values(i)) != values or set(self.block_values(i)) != values:
                result = False

        return result

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += ''.join(str(i) for i in row) + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
