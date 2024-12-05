import time
from datetime import datetime, timezone

from atomic_counter import TimeCounter


class TestTimeCounter:
    def test_time_counter(self):
        counter = TimeCounter()

        # Get first counter value and timestamp
        before_first = datetime.now(timezone.utc)
        first = counter.next()
        first_dt = TimeCounter.to_datetime(first)
        after_first = datetime.now(timezone.utc)

        # Get second counter value and timestamp
        before_second = datetime.now(timezone.utc)
        second = counter.next()
        second_dt = TimeCounter.to_datetime(second)
        after_second = datetime.now(timezone.utc)

        # Basic ordering checks
        assert first < second, "Counter should increase monotonically"
        assert first_dt < second_dt, "Decoded timestamps should increase monotonically"

        # Check that decoded timestamps fall within the expected windows
        assert before_first <= first_dt <= after_first, "First timestamp out of bounds"
        assert before_second <= second_dt <= after_second, "Second timestamp out of bounds"

        # Check counter values for timestamps in same microsecond
        third = counter.next()
        fourth = counter.next()

        assert third < fourth, "Counter should be monotonically increasing"
        third_dt = TimeCounter.to_datetime(third)
        fourth_dt = TimeCounter.to_datetime(fourth)

        if third_dt == fourth_dt:  # If in same microsecond
            third_counter = third & ((1 << 12) - 1)  # Get last 12 bits
            fourth_counter = fourth & ((1 << 12) - 1)
            assert fourth_counter == third_counter + 1, "Counter should increment by 1 within same microsecond"

    def test_timedelta(self):
        counter = TimeCounter()
        assert counter.current() != 0, "First value should not be 0"
        # Below is implementation specific
        assert counter.current() & ((1 << 12) - 1) == 2048, "First call to current should have counter value 2048"

        # Get a series of interleaved timestamps from counter and datetime
        dt1 = datetime.now(timezone.utc)
        val1 = counter.next()

        # Small sleep to ensure timestamps are different
        time.sleep(0.001)

        dt_mid = datetime.now(timezone.utc)
        time.sleep(0.001)

        val2 = counter.next()
        assert val2 & ((1 << 12) - 1) == 0, "First call on microsecond gets counter 0"
        dt2 = datetime.now(timezone.utc)

        assert val1 < val2, "Counter values must be monotonically increasing"

        # Check that our counter timestamps are between the datetime timestamps
        counter_dt1 = TimeCounter.to_datetime(val1)
        counter_dt2 = TimeCounter.to_datetime(val2)

        assert dt1 <= counter_dt1 <= dt2, "First counter timestamp out of bounds"
        assert dt1 <= counter_dt2 <= dt2, "Second counter timestamp out of bounds"

        # Check timedelta
        delta_from_counter = TimeCounter.get_timedelta(val1, val2)
        delta_from_datetime = counter_dt1 - counter_dt2

        assert delta_from_counter == delta_from_datetime, "Timedeltas should match"
        assert delta_from_counter.total_seconds() < 0, "Earlier timestamp minus later should be negative"

        # Check reverse order
        delta_reverse = TimeCounter.get_timedelta(val2, val1)
        assert delta_reverse.total_seconds() > 0, "Later timestamp minus earlier should be positive"
        assert abs(delta_reverse.total_seconds()) == abs(delta_from_counter.total_seconds()), "Absolute timedeltas should be equal"

        assert delta_reverse <= (dt2 - dt1)
        assert (dt_mid - dt1) < delta_reverse
