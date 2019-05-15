# -*- coding: utf-8 -*-
"""
    theworldphone.modules.redis.redis_queue
    ~~~~~~~~~~~~~~~~

    redis module queue class
"""

import redis


class RedisQueue(object):

        def __init__(self, name, **redis_kwargs):
            '''Initializes connection to specified redis queue.
               The default connection parameters are: host='localhost', port=6379, db=0'''
            self.__db = redis.Redis(**redis_kwargs)
            self.key = name

        def qsize(self):
            """Return the size of the queue."""
            return self.__db.llen(self.key)

        def empty(self):
            """Return True if the queue is empty, False otherwise."""
            return self.qsize() == 0

        def push(self, item):
            """Place an item into the queue."""
            self.__db.rpush(self.key, item)

        def pop(self, block=False, timeout=None):
            """Remove and return an item from the queue.
            If optional argument block is true and timeout is None (the default), block
            if necessary until an item becomes available."""
            if block:
                item = self.__db.blpop(self.key, timeout=timeout)
                if item:
                    item = item[1]
            else:
                item = self.__db.lpop(self.key)
            return item

        def rem(self, item):
            self.__db.lrem(self.key, item, 1)

        def all(self):
            return self.__db.lrange(self.key, 0, -1)

        def get_nowait(self):
            """Equivalent to get(False)."""
            return self.get(False)
