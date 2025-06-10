import unittest

from advent_of_code.day_01.__main__ import Day01
from ..advent_testcase import AdventTestCase


class TestDay01(AdventTestCase):

    PUZZLE = Day01

    def test_sample(self):
        result = self.obj()
        self.assertEqual("11", result)


if __name__ == "__main__":
    unittest.main()
