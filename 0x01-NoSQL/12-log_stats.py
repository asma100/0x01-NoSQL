#!/usr/bin/env python3
""" task9 """
from pymongo import MongoClient


def log():
    """ log_
    """
    c = MongoClient('mongodb://127.0.0.1:27017')
    l = c.logs.nginx
    t = l.count_documents({})
    g = l.count_documents({"method": "GET"})
    post = l.count_documents({"method": "POST"})
    put = l.count_documents({"method": "PUT"})
    patch = l.count_documents({"method": "PATCH"})
    d = l.count_documents({"method": "DELETE"})
    path = l.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{t} logs")
    print("Methods:")
    print(f"\tmethod GET: {g}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {d}")
    print(f"{path} status check")


if __name__ == "__main__":
    log()
