#!/usr/bin/env python3
""" tasks """
import uuid
import redis
from typing import Union, Optional, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Storing data in Redis.
    """

    def __init__(self):
        """
        Initializes the cache.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis and returns the generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, int]]:
        """
        Retrieves data and applies a conversion.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        try:
            return int(data)
        except ValueError:
            return data.decode("utf-8")

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data and converts it to a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data and converts it to an integer.
        """
        return self.get(key, fn=int)
