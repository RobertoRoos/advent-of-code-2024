from advent_of_code.shared import Solver, main


class MarketSecrets:
    """Abstractions for the monkey market exchange secrets."""

    @staticmethod
    def mix(secret: int, number: int) -> int:
        return secret ^ number

    @staticmethod
    def prune(secret: int) -> int:
        return secret % 16777216

    @classmethod
    def next_secret(cls, secret: int) -> int:
        """Compute the next secret number."""
        # Step 1:
        new_secret = cls.mix(secret, secret * 64)
        new_secret = cls.prune(new_secret)

        # Step 2:
        new_secret = cls.mix(new_secret, int(new_secret / 32))
        new_secret = cls.prune(new_secret)

        # Step 3:
        new_secret = cls.mix(new_secret, new_secret * 2048)
        new_secret = cls.prune(new_secret)

        return new_secret

    @classmethod
    def next_n_secrets(cls, secret: int, n: int) -> int:
        for _ in range(n):
            secret = cls.next_secret(secret)

        return secret


class Day22(Solver):

    def __call__(self) -> str:
        secrets = [int(txt) for txt in self.iterate_input()]

        new_secrets = [
            MarketSecrets.next_n_secrets(secret, 2_000) for secret in secrets
        ]

        result = sum(new_secrets)

        return str(result)


if __name__ == "__main__":
    main(Day22)
