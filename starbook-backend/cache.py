from redis import StrictRedis

from hash_with_lru import HashWithLru
from env import *


class Cache:
    def __init__(self):
        self.redis = StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'],
                                 db=os.environ['REDIS_DB_NUM'])
        self.queries_cache = HashWithLru('queries', int(os.environ['QUERIES_CACHE_SIZE']), self.redis)

    def clear_cache(self):
        self.redis.hset(USAGE_COUNTER, REDIS_RESPONSE_TREE_KEY, 0)
        self.queries_cache.clear()
