# Atomic Counter

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

c = Counter(offset_in_nanos, base_in_nanos)

c.next()  # generate next number in sequence
```

Here, `base` is the counter's `0` value (e.g. a epoch in nanos to consider the `0` point, to keep numbers as small as possible if you do not need to go back to 1970). `offset` is the number of nanos since `base` at which to start.

If unset, `base` will be `2010-01-01` in nanos, `offset` will be `0`, which means the counter will start at `(now - 2010/01/01) as nanos`.

To create e.g. a daily counter, pass in `base=today in nanos`. As this is a common occurrence for sequences that reset daily, a convenience function `def daily() -> Counter:` is provided.



