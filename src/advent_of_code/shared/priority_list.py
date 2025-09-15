from heapq import heappop, heappush
from typing import Generic, List, Tuple, TypeVar

T = TypeVar("T")  # The list item type


class PriorityList(Generic[T]):
    """Class abstraction heapq priority list.

    We keep a list with a priority for each item, with a guarantee that the lowest
    priority item is always ready.
    Items in the list are _never_ compared. If two entries have equal priority,
    the one that was added first will be at the front! But this should not be relied
    upon!
    """

    def __init__(self):
        self._data: List[Tuple[int, int, T]] = []
        # ^ like `[(<priority>, <counter>, <entry>), ... ]`
        self._counter = 0  # Counter, just to avoid accidentally comparing entries

    @property
    def data(self):
        return self._data

    def push(self, priority: int, entry: T):
        heappush(self._data, (priority, self._counter, entry))
        self._counter += 1

    def pop(self) -> Tuple[int, T]:
        priority, _, entry = heappop(self._data)
        return priority, entry

    def reset(self):
        self._data = []
        self._counter = 0

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)
