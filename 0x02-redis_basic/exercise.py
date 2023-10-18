#!/usr/bin/env python3
'''
Module: 'exercise'
Class named 'Cache'
'''

import redis
from uuid import uuid4


class Cache():
    '''Represents class Cache'''

    def __init__(self) -> None:
        '''Instantiation'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str | bytes | int | float) -> str:
        '''Returns a string that is associated with a key'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key
