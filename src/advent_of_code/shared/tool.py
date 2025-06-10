import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Iterator, List, Type


class Tool:
    """Shared base class for a CLI for any puzzle solution."""

    NAME = "__main__"

    def __init__(self, *args, **kwargs):
        self.argument_parser: None | ArgumentParser = None
        self.args: None | Namespace = None

        self.argument_parser = self.make_parser()
        self.args = self.argument_parser.parse_args(*args, **kwargs)
        self.input_file = Path(self.args.input_file)
        with open(self.input_file):
            pass  # Assert file exists

    @classmethod
    def make_parser(cls) -> ArgumentParser:
        parser = ArgumentParser(
            prog=cls.__name__, description="Advent of code 2024 solution for this day."
        )
        parser.add_argument(
            "input_file",
            help="Path to input file to use",
        )
        return parser

    def iterate_input(self) -> Iterator[str]:
        """Yield each line of the input file."""
        with open(self.input_file, "r") as fh:
            while line := fh.readline():
                yield line

    def get_input(self) -> List[str]:
        return self.input_file.read_text().split("\n")

    def __call__(self) -> str:
        """Magic method for object execution, which will do the puzzle solving."""
        raise NotImplementedError("Class call method must be implemented")


def main(cli_class: Type[Tool]):
    """Pass a class and execute it (if this is being run as main)."""
    cli_object = cli_class(sys.argv[1:])
    result = cli_object()
    print("Answer:", result)
