from time import perf_counter_ns
from typing import Callable


def measure_time_ns(func: Callable) -> Callable:
    def wrapper():
        start = perf_counter_ns()
        func()
        end = perf_counter_ns()
        # FIXME: Change to logging.
        print(f'Total time elapsed for {func.__name__}: {end - start} nanoseconds.')

    return wrapper
