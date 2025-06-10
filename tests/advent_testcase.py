import inspect
from abc import ABCMeta
from pathlib import Path
from typing import Type
from unittest import TestCase

from advent_of_code.shared import Tool


class AdventTestCase(TestCase, metaclass=ABCMeta):
    """Abstract test case for any puzzle implementation."""

    PUZZLE: Type | None = None

    def setUp(self):
        # Get the .txt file next to the test file:
        test_file = Path(inspect.getfile(self.__class__)).absolute()
        self.input_file = test_file.parent / "input.txt"
        self.obj: Tool = self.PUZZLE([str(self.input_file)])
