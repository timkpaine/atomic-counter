from datetime import datetime

from atomic_counter import daily


class TestOffset:
    def test_bounds(self):
        counter = daily()
        nowish = datetime.utcnow()
        seconds_today = nowish.second + nowish.minute * 60 + nowish.hour * 3600

        # offset for small delay
        seconds_today += 1

        # convert to nanos
        nanos_today = seconds_today * 1_000_000_000
        assert 1_000_000_000 < counter.next() < nanos_today
