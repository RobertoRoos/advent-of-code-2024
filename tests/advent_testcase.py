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

    def get_solver(self, part: int = 1) -> Solver:
        """Return solver instance based on ``PUZZLE`` variable."""
        # Get the .txt file next to the test file:
        test_file = Path(inspect.getfile(self.__class__)).absolute()
        input_file = test_file.parent / "sample_input.txt"
        return self.PUZZLE([str(input_file), "--part", str(part)])
