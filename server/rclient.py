from collections.abc import Iterable

import redis
from server.client import GameClient

WORLD_KEY = 'world'
WORLD_VERSION_KEY = 'world_version'

class RedisClient(GameClient):
    def __init__(self, host, port, world_size: int, username=None, pw=None) -> None:
        self.redis = redis.Redis(host=host, port=port, db=0, decode_responses=True, username=username, password=pw)
                
        # Worldgen Stuff
        if not self.redis.exists(WORLD_KEY):
            for x in range(world_size):
                for z in range(world_size):
                    self.send_block([x, 0, z], "stone.png")


    def get_world(self) -> Iterable[list[any]]:
        world = self.redis.hgetall(WORLD_KEY)
        for key, value in world.items():
            x, y, z = [int(i) for i in key.split(",")]
            yield [x, y, z, value]


    def get_world_version(self) -> int:
        return int(self.redis.get(WORLD_VERSION_KEY) or 0)


    def get_world_edits(self) -> list[list[any]]:
        raise NotImplementedError


    def send_block(self, position, tex) -> None:
        key = ",".join([str(int(i)) for i in position])
        self.redis.hset(WORLD_KEY, key, tex)
        self.redis.incr(WORLD_VERSION_KEY)


    def send_destroy(self, position, tex) -> None:
        key = ",".join([str(int(i)) for i in position])
        self.redis.hdel(WORLD_KEY, key)
        self.redis.incr(WORLD_VERSION_KEY)
