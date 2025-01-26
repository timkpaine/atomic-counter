# atomic counter

Atomic Counters

[![Build Status](https://github.com/timkpaine/atomic-counter/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/timkpaine/atomic-counter/actions/workflows/build.yml)
[![Build Status](https://github.com/timkpaine/atomic-counter/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/timkpaine/atomic-counter/actions?query=workflow%3A%22Build+Status%22)
[![Coverage](https://codecov.io/gh/timkpaine/atomic-counter/branch/main/graph/badge.svg)](https://codecov.io/gh/timkpaine/atomic-counter)
[![License](https://img.shields.io/github/license/timkpaine/atomic-counter.svg)](https://pypi.python.org/pypi/atomic-counter)
[![PyPI](https://img.shields.io/pypi/v/atomic-counter.svg)](https://pypi.python.org/pypi/atomic-counter)

## Overview
`atomic-counter` is a rust library for generating a monotonically increasing sequence of integers. Depending on the particular configuration of the counter, the generated sequence will be produce unique numbers down to the nanosecond, regardless of memory state.
E.g. if you quit the process and recreate a new counter `>1ns` later, your sequence is guaranteed to still be monotonically increasing (but with a gap).

## Usage

```python
from atomic_counter import Counter

c = Counter(base_in_nanos)

c.next()  # generate next number in sequence
```

To create e.g. a daily counter, pass in `base=today in nanos`. As this is a common occurrence for sequences that reset daily, a convenience function `def daily() -> Counter:` is provided.


There is also a `TimeCounter` class provided. A 64 bit unsigned integer is created that is monotonically increasing, and allows for converting to microseconds to serve as a timestamp (up to the year 2112). Will break if more than 4096 calls to "next" are called within a single microsecond (which is almost assuredly never going to be physically possible, every call makes a system call to get the current time).

```python
from atomic_counter import TimeCounter
from datetime import datetime, timezone

c = TimeCounter()

x = c.next()  # generate id
x_time = TimeCounter.to_datetime(x)  # generates the datetime where the value was called.
now = datetime.now(timezone.utc)
assert x_time <= now
```

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
