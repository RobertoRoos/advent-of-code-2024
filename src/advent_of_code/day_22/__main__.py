from collections import defaultdict
from typing import Dict, Iterable, Set, Tuple

from advent_of_code.shared import Solver, main


class MarketSecrets:
    """Abstractions for the monkey market exchange secrets."""

    @staticmethod
    def mix(secret: int, number: int) -> int:
        return secret ^ number

    @staticmethod
    def prune(secret: int) -> int:
        # Note: 16777216 = 2^24
        return secret % 16777216

    @classmethod
    def next_secret(cls, secret: int) -> int:
        """Compute the next secret number."""
        # Step 1:
        # new_secret = cls.mix(secret, secret * 64)
        # new_secret = cls.prune(new_secret)
        new_secret = (secret ^ (secret << 6)) & 16777215

        # Condensing these steps is slightly faster
        # Now that multiplying by 2^n is the same as a bit-shift and a modulo of
        # 2^n is the same as a bitmask

        # Step 2:
        # new_secret = cls.mix(new_secret, int(new_secret / 32))
        # new_secret = cls.prune(new_secret)
        new_secret = (new_secret ^ (new_secret >> 5)) & 16777215

        # Step 3:
        # new_secret = cls.mix(new_secret, new_secret * 2048)
        # new_secret = cls.prune(new_secret)
        new_secret = (new_secret ^ (new_secret << 11)) & 16777215

        return new_secret

    @classmethod
    def get_n_secrets(cls, secret: int, n: int) -> Iterable[int]:
        """Get a list of `N` following secrets."""
        yield secret
        for _ in range(n):
            secret = cls.next_secret(secret)
            yield secret

    @staticmethod
    def get_price(secret: int) -> int:
        return secret % 10


class Day22(Solver):

    def __call__(self) -> str:
        starting_secrets = [int(txt) for txt in self.iterate_input()]

        if self.args.part == 1:
            result = 0

            for starting_secret in starting_secrets:
                _final_secret = 0
                for _final_secret in MarketSecrets.get_n_secrets(
                    starting_secret, 2_000
                ):
                    pass
                result += _final_secret

            return str(result)

        else:
            sum_prices_by_changes_sum: Dict[Tuple, int] = defaultdict(int)
            # Prices by price changes, summed together, like:
            # { (<w>, <x>, <y>, <z>): <sum of prices>, ... }

            for _buyer, starting_secret in enumerate(starting_secrets):
                changes: Tuple = tuple([0] * 4)
                changes_seen: Set[Tuple] = set()
                prev_price = None
                for i, secret in enumerate(
                    MarketSecrets.get_n_secrets(starting_secret, 2_000)
                ):
                    price = MarketSecrets.get_price(secret)
                    if prev_price is not None:
                        changes = tuple(
                            [changes[1], changes[2], changes[3], price - prev_price]
                        )

                    if i > 3:
                        if changes not in changes_seen:
                            sum_prices_by_changes_sum[changes] += price
                            changes_seen.add(changes)

                    prev_price = price

            changes = max(sum_prices_by_changes_sum, key=sum_prices_by_changes_sum.get)
            result = sum_prices_by_changes_sum[changes]

            return str(result)


if __name__ == "__main__":
    main(Day22)
