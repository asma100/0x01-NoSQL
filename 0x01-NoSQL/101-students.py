#!/usr/bin/env python3
""" task9 """
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Finds all students in a collection
    """
    students = mongo_collection.aggregate([
        {
            '$project': {
                '_id': 1,
                'name': 1,
                'averageScore': {
                    '$avg': '$topics.score',
                }
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ])
    return list(students)
