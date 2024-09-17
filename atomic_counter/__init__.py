__version__ = "0.1.3"

from datetime import datetime

from .atomic_counter import Counter

_BASE = 1577854800000000000


def daily() -> Counter:
    """Generate a counter which is guaranteed to produce unique numbers
    for a single day, regardless of instantiation time, up to a granularity
    of 1ns"""

    nowish = datetime.utcnow()
    base = datetime(nowish.year, nowish.month, nowish.day)

    return Counter(int(base.timestamp()) * 1_000_000_000)


__all__ = [
    "Counter",
    "daily",
]
