#!/usr/bin/env python3
'''
n this tasks, we will implement a get_page function (prototype:
def get_page(url: str) -> str:). The core of the function is very simple.
It uses the requests module to obtain the HTML content of a particular
URL and returns it.

Start in a new file named web.py and do not reuse the code written in
exercise.py.

Inside get_page track how many times a particular URL was accessed in the
key "count:{url}" and cache the result with an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response and
test your caching.

Bonus: implement this use case with decorators.
'''

import redis
import requests
from time import time
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(func):
    '''
    Decorator to cache the page and count its access
    '''
    @wraps(func)
    def wrapper(url: str):
        # Check if the URL content is cached
        cached_content = redis_client.get(url)

        # If cached content exists, return it
        if cached_content:
            redis_client.incr(f"count:{url}")  # Increment the access count
            # Return the cached content as a string
            return cached_content.decode('utf-8')

        # If content is not cached, fetch it from the web
        response = func(url)

        # Cache the fetched content for 10 seconds
        redis_client.setex(url, 10, response)

        # Increment the access count for the URL
        redis_client.incr(f"count:{url}")

        return response

    return wrapper


@cache_page
def get_page(url: str) -> str:
    '''
    Fetch the HTML content of a URL.
    '''
    response = requests.get(url)
    return response.text
