#!/usr/bin/env python3
'''
Module: 'web'
'''

import requests
import redis
from typing import Optional

# Initialize the Redis connection
redis_client = redis.Redis()


def get_page(url: str) -> str:
    '''Define the key for tracking URL access count'''
    count_key = f"count:{url}"

    # Check if the count key exists in Redis
    if redis_client.exists(count_key):
        # If the count key exists, increment the count
        redis_client.incr(count_key)
    else:
        # If the count key doesn't exist, set it to 1 with a 10-second expiration
        redis_client.setex(count_key, 10, 1)

    # Use the requests library to fetch the HTML content of the URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch URL: {url}"
