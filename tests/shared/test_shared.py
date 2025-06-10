import contextlib
import io
import unittest

from advent_of_code.shared import Tool

from ..advent_testcase import AdventTestCase


class Day00(Tool):
    """Dummy puzzle implementation."""

    def __call__(self, *args, **kwargs):
        return 42


class TestDay00Bare(unittest.TestCase):

    def test_help(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit):
                _ = Day00(["--help"])

        txt = f.getvalue()
        self.assertTrue(txt.startswith("usage: "))


class TestDay00(AdventTestCase):

    PUZZLE = Day00

    def test_call(self):
        result = self.obj()

        self.assertEqual(42, result)

    def test_input(self):
        txt = "\n".join(list(self.obj.iterate_input()))
        self.assertEqual("test\n", txt)


if __name__ == "__main__":
    unittest.main()
