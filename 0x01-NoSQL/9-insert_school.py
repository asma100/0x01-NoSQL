#!/usr/bin/env python3
""" task9 """


def insert_school(mongo_collection, **kwargs):
    """
        retrieve all documents

    """
    x = mongo_collection.insert_one(kwargs)
    return x.inserted_id
