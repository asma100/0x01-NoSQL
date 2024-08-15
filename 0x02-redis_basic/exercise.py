#!/usr/bin/env python3
""" tasks """
import uuid
import redis
from typing import Union, Optional, Callable
from functools import wraps


class Cache:
    """
    A cache class that stores data in Redis and provides methods for retrieval with conversion.
    """

    def __init__(self):
        """
        Initializes the cache with a Redis connection.
        """
        self._redis = redis.Redis()
        self.method_calls = {}  # Dictionary to store method call counts

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis and returns the generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @count_calls
    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, int]]:
        """
        Retrieves data and applies an  conversion .
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
        Retrieves data  and converts it to a string.
        """

        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data converts it to an integer.
        """

        return self.get(key, fn=int)

    def count_calls(self, method):
        """
        counts calls to a method and returns a wrapped function.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            method_name = method.__qualname__
            self.method_calls[method_name] = self.method_calls.get(method_name, 0) + 1
            return method(self, *args, **kwargs)

        return wrapper
