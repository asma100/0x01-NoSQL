#!/usr/bin/env python3
""" task9 """
import uuid
import redis
from typing import Union


class Cache:
    """
    storing data.
    """

    def __init__(self):
        """
        Initializes the cache
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis and returns the generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
