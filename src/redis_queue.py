import json

import redis


class RedisQueue:
    def __init__(self, queue_name):
        self.__r = redis.Redis(
            host="localhost",
            port=6379
        )
        self.queue_name = queue_name

    def publish(self, msg: dict):
        self.__r.rpush(self.queue_name, json.dumps(msg))

    def consume(self) -> dict:
        response = self.__r.blpop(self.queue_name)
        if response:
            return json.loads(response[1])
        return None


if __name__ == '__main__':
    q = RedisQueue(queue_name="fifo_queue")
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
