from redis import StrictRedis
from linked_list import LinkedList
from node import Node

LINKED_LIST = 'linked_list'


class HashWithLru:
    def __init__(self, hash_name, max_size, redis=StrictRedis()):
        self.hash_name = hash_name
        self.linked_list = LinkedList()
        self.max_size = max_size
        self.redis = redis
        self.nodes = {}

    def get(self, key):
        val = self.redis.hget(self.hash_name, key)
        if val is None:
            return
        self._touch(key)
        return val

    def set(self, key, value):
        self.redis.hset(self.hash_name, key, value)
        self._touch(key)

    def clear(self):
        self.redis.delete(self.hash_name)
        self.linked_list = LinkedList()
        self.nodes = {}

    def _touch(self, key):
        node = self.nodes.get(key, None)
        if node:
            self.linked_list.remove(node)
            del self.nodes[key]

        new_node = Node(key)
        self.linked_list.push_first(new_node)
        self.nodes[key] = new_node

        if self.linked_list.size > self.max_size:
            node = self.linked_list.pop_last()
            del self.nodes[node.data]
            self.redis.hdel(self.hash_name, node.data)

    def print(self):
        self.linked_list.print()
        print('\n{}\n'.format(self.nodes.keys()))


if __name__ == '__main__':
    h = HashWithLru('my_hash', 4, StrictRedis(db=1))
    h.redis.flushdb()
    for i in range(6):
        print(h.get('key{}'.format(i)))
    for i in range(6):
        h.set('key{}'.format(i), 'val{}'.format(i))
    for i in range(6):
        print(h.get('key{}'.format(i)))
        h.print()
    h.clear()
