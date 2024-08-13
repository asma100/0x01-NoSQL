#!/usr/bin/env python3
""" task9 """


def schools_by_topic(mongo_collection, topic):
    """
        FUNC

    """
    f = {"topics": {"$in": [topic]}}
    return list(mongo_collection.find(f))
