import unittest

from advent_of_code.day_05.__main__ import Day05, Page

from ..advent_testcase import AdventTestCase


class TestDay05(AdventTestCase):

    PUZZLE = Day05

    def setUp(self):
        Page.ORDER.clear()

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("143", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2)
        result = solver()
        self.assertEqual("123", result)

    def test_page_hash(self):
        my_set = {Page(10), Page(15), Page(9)}
        self.assertTrue(Page(15) in my_set)

    def test_page_sort(self):
        Page.ORDER[9] = {Page(5), Page(2)}
        Page.ORDER[5] = {Page(2), Page(1)}
        Page.ORDER[4] = {Page(2)}
        self.assertTrue(Page(9) < Page(5))
        self.assertTrue(Page(5) < Page(2))


if __name__ == "__main__":
    unittest.main()
