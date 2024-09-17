from datetime import datetime

from atomic_counter import _BASE, Counter


class TestOffset:
    def test_base(self):
        c = Counter(0, 0)
        assert c.current() == 0
        assert c.next() == 1
        assert c.current() == 1

    def test_interval(self):
        c1 = Counter(None, _BASE, 2)
        c2 = Counter(None, _BASE + 1, 2)
        assert c1.current() == 0
        assert c2.current() == 1
        assert c1.next() == 2
        assert c2.next() == 3
        assert c1.current() == 2
        assert c2.current() == 3

    def test_offset(self):
        nowish = datetime.utcnow()
        base = datetime(nowish.year, nowish.month, nowish.day, nowish.hour, nowish.minute, nowish.second, nowish.microsecond)
        nowish2 = datetime(nowish.year, nowish.month, nowish.day, nowish.hour, nowish.minute, nowish.second + 1, nowish.microsecond)
        base = int(base.timestamp()) * 1_000_000_000
        nowish = int(nowish.timestamp()) * 1_000_000_000
        nowish2 = int(nowish2.timestamp()) * 1_000_000_000
        c = Counter(base, nowish)

        # if we offset to the nearest second, we should be within 1s
        assert c.current() <= 1_000
        assert c.next() <= 1_000

        c = Counter(nowish, nowish2)

        # if we offset to the nearest second, we should be within 1s
        assert c.next() == 1_000_000_001
