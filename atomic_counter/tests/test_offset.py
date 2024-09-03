from atomic_counter import Counter
from datetime import datetime
from dateutil import tz


class TestOffset:
    def test_base(self):
        nowish = datetime.now()
        base = datetime(nowish.year, nowish.month, nowish.day, tzinfo=tz.UTC)

        c = Counter(None, int(base.timestamp()) * 1_000_000)
        assert c.current() == 0
        assert c.next() == 1
        assert c.current() == 1

    def test_offset(self):
        nowish = datetime.utcnow()
        base = datetime(nowish.year, nowish.month, nowish.day, tzinfo=tz.UTC)
        offset = (datetime(nowish.year, nowish.month, nowish.day, nowish.hour, nowish.minute, nowish.second, tzinfo=tz.UTC) - base).total_seconds()

        offset = int(offset) * 1_000_000_000
        base = int(base.timestamp()) * 1_000_000_000
        nowish = int(nowish.timestamp()) * 1_000_000_000

        c = Counter(offset, base)

        # if we offset to the nearest second, we should be within 1s
        assert c.next() <= 1_000_000_000

    def test_interval(self):
        c1 = Counter(None, 0, 2)
        c2 = Counter(None, 0, 2)
        c1.set(0)
        c2.set(1)
        assert c1.current() == 0
        assert c2.current() == 1
        assert c1.next() == 2
        assert c2.next() == 3
        assert c1.current() == 2
        assert c2.current() == 3
