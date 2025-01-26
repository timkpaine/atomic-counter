from contextlib import contextmanager
from time import perf_counter

from atomic_counter import Counter


@contextmanager
def timer():
    t1 = t2 = perf_counter()
    yield lambda: t2 - t1
    t2 = perf_counter()


def main():
    measures = []
    for _ in range(5):
        with timer() as t:
            counter = Counter()
            for i in range(2 * 10**6):
                counter.next()
        measures.append(t())
        print(f"Time taken: {measures[-1]:.4f} seconds")
    print(f"Average time taken: {sum(measures) / len(measures):.4f} seconds")


if __name__ == "__main__":
    main()
