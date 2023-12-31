#!/usr/bin/env python3
'''
Module: 'exercise'
Class named 'Cache'
'''

import redis
from uuid import uuid4
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Counts the number of calls to class Cache'''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Calls the given method after incrementing call counter'''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_list_key = f"{method.__qualname__}:inputs"
        output_list_key = f"{method.__qualname__}:outputs"

        # Convert input arguments to strings and append to the input list
        self._redis.rpush(input_list_key, str(args))

        # Execute the wrapped function to retrieve the output
        result = method(self, *args, **kwargs)

        # Store the output in the output list
        self._redis.rpush(output_list_key, result)

        return result

    return wrapper


class Cache():
    '''Represents class Cache'''

    def __init__(self) -> None:
        '''Instantiation'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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


def replay(fn: Callable) -> None:
    '''Get the function's qualified name to find the input and output lists'''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    method_name = fn.__qualname__
    input_list_key = f"{method_name}:inputs"
    output_list_key = f"{method_name}:outputs"

    inputs = cache._redis.lrange(input_list_key, 0, -1)
    outputs = cache._redis.lrange(output_list_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(f"{method_name}(*{eval(args.decode())}) -> {output.decode()}")
