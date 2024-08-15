
#!/usr/bin/env python3
"""tasks"""
import requests
import redis
import functools
from typing import Callable

r = redis.Redis()

def cache_with_expiration(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of the function in Redis with an expiration time.
    """
    def decorator(method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(url: str) -> str:
            cache_key = f"cache:{url}"
            cached_page = r.get(cache_key)

            if cached_page:
                return cached_page.decode('utf-8')

            result = method(url)
            r.setex(cache_key, expiration, result)
            return result

        return wrapper

    return decorator

def count_access(method: Callable) -> Callable:
    """
    Decorator to count the number of times a particular URL is accessed.
    """
    @functools.wraps(method)
    def wrapper(url: str) -> str:
        access_key = f"count:{url}"
        r.incr(access_key)
        return method(url)

    return wrapper

@cache_with_expiration(10)
@count_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL and caches the result.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    
    print("First access (should be slow):")
    print(get_page(test_url))
    
    print("\nSecond access (should be fast from cache):")
    print(get_page(test_url))

    print("\nAccess count:")
    print(r.get(f"count:{test_url}").decode('utf-8'))
