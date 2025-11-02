import datetime
import time
import uuid
from functools import wraps

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def single(max_processing_time):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            unique_value = str(uuid.uuid4())
            acquired = r.set(
                name=func.__name__,
                value=unique_value,
                nx=True,
                ex=int(max_processing_time.total_seconds()),
            )
            if not acquired:
                raise RuntimeError(
                    f"Func {func.__name__} already running on another server. "
                )

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print(f"Exception in func: {e}")
                raise
            finally:
                current_value = r.get(func.__name__)
                if current_value == unique_value:
                    r.delete(func.__name__)
        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(seconds=20))
def process_transaction():
    time.sleep(50)
