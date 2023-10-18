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
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def wrapper(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_client.incr(f'count:{url}')
        result = redis_client.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_client.set(f'count:{url}', 0)
        redis_client.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
