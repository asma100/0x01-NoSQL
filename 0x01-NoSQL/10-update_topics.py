#!/usr/bin/env python3
""" task9 """


def update_topics(mongo_collection, name, topics):
    """
        retrieve all documents

    """
    filter = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_many(filter, update)
