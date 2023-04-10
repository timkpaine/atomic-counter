__version__ = "0.1.1"

from functools import lru_cache
from datetime import datetime
from dateutil import tz

from .atomic_counter import Counter


def daily() -> Counter:
    '''Generate a counter which is guaranteed to produce unique numbers
    for a single day, regardless of instantiation time, up to a granularity
    of 1ns'''

    nowish = datetime.utcnow()
    base = datetime(nowish.year, nowish.month, nowish.day, tzinfo=tz.UTC)

    return Counter(0, int(base.timestamp()) * 1_000_000_000)

__all__ = [
    "Counter",
    "daily",
]
