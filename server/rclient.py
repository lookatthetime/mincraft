from collections.abc import Iterable

import redis

WORLD_KEY = 'world'
WORLD_VERSION_KEY = 'world_version'

class RedisClient:
    def __init__(self, host, port, username=None, pw=None) -> None:
        self.redis = redis.Redis(host=host, port=port, db=0, decode_responses=True, username=username, password=pw)


    def get_world(self) -> Iterable[list[any]]:
        world = self.redis.hgetall(WORLD_KEY)
        for key, value in world.items():
            x, y, z = [int(i) for i in key.split(",")]
            yield [x, y, z, value]


    def get_world_version(self) -> int:
        return int(self.redis.get(WORLD_VERSION_KEY) or 0)


    def send_block(self, position, tex) -> None:
        key = ",".join([str(int(i)) for i in position])
        self.redis.hset(WORLD_KEY, key, tex)
        self.redis.incr(WORLD_VERSION_KEY)


    def send_destroy(self, position, tex) -> None:
        key = ",".join([str(int(i)) for i in position])
        self.redis.hdel(WORLD_KEY, key)
        self.redis.incr(WORLD_VERSION_KEY)
