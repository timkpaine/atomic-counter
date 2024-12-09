__version__ = "0.1.4"

from datetime import datetime, timedelta, timezone

from .atomic_counter import Counter, TimeCounter

_BASE = 1577854800000000000


def to_datetime(value: int) -> datetime:
    micros = TimeCounter.decode_timestamp_microseconds(value)
    return datetime.fromtimestamp(micros / 1e6, tz=timezone.utc)


def get_timedelta(later: int, earlier: int) -> timedelta:
    return to_datetime(later) - to_datetime(earlier)


TimeCounter.to_datetime = staticmethod(to_datetime)
TimeCounter.get_timedelta = staticmethod(get_timedelta)


def daily() -> Counter:
    """Generate a counter which is guaranteed to produce unique numbers
    for a single day, regardless of instantiation time, up to a granularity
    of 1ns"""

    nowish = datetime.now(timezone.utc)
    base = datetime(nowish.year, nowish.month, nowish.day, tzinfo=timezone.utc)

    return Counter(int(base.timestamp()) * 1_000_000_000)


__all__ = [
    "Counter",
    "TimeCounter",
    "daily",
]
