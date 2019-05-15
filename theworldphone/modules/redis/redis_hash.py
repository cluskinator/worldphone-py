# -*- coding: utf-8 -*-
"""
    theworldphone.modules.redis.redis_hash
    ~~~~~~~~~~~~~~~~

    redis module hash class
"""

import redis


class RedisHash(object):

    def __init__(self, name, **redis_kwargs):
        '''Initializes connection to specified redis queue.
        The default connection parameters are: host='localhost', port=6379, db=0'''
        self.__db = redis.Redis(**redis_kwargs)
        self.__key = name

    def put(self, field, value):
        '''Place an item into the hash.
        Returns true if the field does not exist, false otherwise.
        '''
        if self.__db.hsetnx(self.__key, field, value):
            return True
        else:
            return False

    def over_put(self, field, value):
        '''Place an item into the hash. Overrides the existing value.'''
        self.__db.hset(self.__key, field, value)

    def qsize(self):
        '''Return the size of the request id queue.'''
        return self.__db.hlen(self.__key)

    def empty(self):
        '''Return True if the request queue is empty, False otherwise.'''
        return self.__db.hlen(self.__key) == 0

    def exists(self, field):
        '''Returns True if a field exists, false otherwise.'''
        return self.__db.hexists(self.__key, field)

    def get(self, field):
        '''Returns value for a given field.'''
        return self.__db.hget(self.__key, field)

    def rem(self, *field):
        '''Removes the given field(s) from the hash.'''
        return self.__db.hdel(self.__key, *field)

    def getall(self):
        '''Returns all items from the hash.'''
        return self.__db.hgetall(self.__key)

    def getall_fields(self):
        '''Returns all items fields from the hash.'''
        return self.__db.hkeys(self.__key)
