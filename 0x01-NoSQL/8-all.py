#!/usr/bin/env python3
""" task8 """


def list_all(mongo_collection):
    """
    retrieve all documents

    """
    return mongo_collection.find()
