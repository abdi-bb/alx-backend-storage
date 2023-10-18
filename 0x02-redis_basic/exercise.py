#!/usr/bin/env python3
'''
Module: 'exercise'
Class named 'Cache'
'''

import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # Use the qualified name of the method as the key
        count = int(self._redis.get(key) or 0)
        count += 1
        self._redis.set(key, count)
        return method(self, *args, **kwargs)
    return wrapper


class Cache():
    '''Represents class Cache'''

    def __init__(self) -> None:
        '''Instantiation'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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
