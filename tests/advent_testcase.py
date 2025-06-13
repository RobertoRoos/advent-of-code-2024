import inspect
from abc import ABCMeta
from pathlib import Path
from typing import Type
from unittest import TestCase

from advent_of_code.shared import Solver


class AdventTestCase(TestCase, metaclass=ABCMeta):
    """Abstract test case for any puzzle implementation."""

    PUZZLE: Type | None = None

    def setUp(self):
        pass

    def get_solver(
        self, part: int = 1, input_file: str | Path = "sample_input.txt"
    ) -> Solver:
        """Return solver instance based on ``PUZZLE`` variable."""
        # Get the .txt file next to the test file:
        test_file = Path(inspect.getfile(self.__class__)).absolute()
        if isinstance(input_file, str) or not input_file.is_absolute():
            input_file = test_file.parent / Path(input_file)
        return self.PUZZLE([str(input_file), "--part", str(part)])
