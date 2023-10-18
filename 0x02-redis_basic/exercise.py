#!/usr/bin/env python3
'''
Module: 'exercise'
Class named 'Cache'
'''

import redis
from uuid import uuid4
from typing import Union, Callable


class Cache():
    '''Represents class Cache'''

    def __init__(self) -> None:
        '''Instantiation'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Returns a string that is associated with a key'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        '''Converts data back to the desired format'''
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''Returns str from a given data'''
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Returns int'''
        return self.get(key, fn=lambda d: int(d))
