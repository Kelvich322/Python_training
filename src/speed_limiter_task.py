import random
import time
import uuid

import redis

r = redis.Redis()

class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def test(self) -> bool:
        curr_time = int(time.time() * 1000)
        window_start = curr_time - 3000

        pipe = r.pipeline()
        pipe.zremrangebyscore("RateLimiter", "-inf", window_start)
        pipe.zcard("RateLimiter")
        results = pipe.execute()
        current_count = results[1]
        if current_count < 5:
            r.zadd("RateLimiter", {str(uuid.uuid4()): curr_time})
            r.expire("RateLimiter", 4)
            return True
        return False

def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")

