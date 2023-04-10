from atomic_counter import Counter
from datetime import datetime
from dateutil import tz 


class TestOffset:
    def test_base(self):
        nowish = datetime.now()
        base = datetime(nowish.year, nowish.month, nowish.day, tzinfo=tz.UTC)

        c = Counter(None, int(base.timestamp()) * 1_000_000)
        assert c.next() == 0

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


