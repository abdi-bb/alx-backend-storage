#!/usr/bin/env python3
'''
Module: 'web'
'''

import requests
import redis
from functools import wraps
from typing import Callable


# Initialize the Redis connection
redis_client = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data and tracks the request count.
    '''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Wrapper for caching and tracking.
        '''
        count_key = f'count:{url}'
        result_key = f'result:{url}'

        redis_client.incr(count_key)
        cached_result = redis_client.get(result_key)

        if cached_result:
            return cached_result.decode('utf-8')

        result = method(url)

        redis_client.set(count_key, 0)
        redis_client.setex(result_key, 10, result)

        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching and tracking the request.
    '''
    return requests.get(url).text
