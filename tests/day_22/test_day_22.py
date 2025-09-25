import unittest

from advent_of_code.day_22.__main__ import Day22, MarketSecrets

from ..advent_testcase import AdventTestCase


class TestDay22(AdventTestCase):

    PUZZLE = Day22

    def test_operations(self):
        self.assertEqual(
            37,
            MarketSecrets.mix(42, 15),
        )
        self.assertEqual(
            16113920,
            MarketSecrets.prune(100000000),
        )

    def test_secrets_sequence(self):
        secret = 123

        expected = [
            15887950,
            16495136,
            527345,
            704524,
            1553684,
            12683156,
            11100544,
            12249484,
            7753432,
            5908254,
        ]

        result = []
        for _ in expected:
            secret = MarketSecrets.next_secret(secret)
            result.append(secret)

        self.assertEqual(expected, result)

    def test_sample_part_1(self):
        solver = self.get_solver(1)
        result = solver()
        self.assertEqual("37327623", result)

    def test_sample_part_2(self):
        solver = self.get_solver(2, input_file="sample_input_part_2.txt")
        result = solver()
        self.assertEqual("23", result)


if __name__ == "__main__":
    unittest.main()
