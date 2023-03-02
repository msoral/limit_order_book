from time import perf_counter_ns
from typing import Callable

from loguru import logger


def measure_time_ns(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = perf_counter_ns()
        returned_value = func(*args, **kwargs)
        end = perf_counter_ns()
        logger.info(f'Total time elapsed {func.__name__}: {end - start} nanoseconds.')
        return returned_value

    return wrapper
