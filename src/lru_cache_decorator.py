import unittest.mock
from functools import wraps


def lru_cache(func=None, *, maxsize=None):
    if func is None:
        return lambda f: lru_cache(f, maxsize=maxsize)

    counter = 0
    cache_dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal counter, cache_dict

        sorted_kwargs = tuple(sorted(kwargs.items()))
        key = (args, sorted_kwargs)

        if key in cache_dict:
            counter += 1
            cache_dict[key][1] = counter
            return cache_dict[key][0]

        counter += 1
        cache_dict[key] = [func(*args, **kwargs), counter]

        if maxsize and len(cache_dict) > maxsize:
            min_key = None
            min_call_count = counter
            for k, v in cache_dict.items():
                if v[1] < min_call_count:
                    min_call_count = v[1]
                    min_key = k

            if min_key:
                del cache_dict[min_key]

        return cache_dict[key][0]

    return wrapper


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
