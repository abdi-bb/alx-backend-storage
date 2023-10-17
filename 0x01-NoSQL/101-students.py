#!/usr/bin/env python3
'''
Module: '101-students'
'''


from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Get all students sorted by average score in descending order.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection of students.

    Returns:
        list: List of students sorted by average score.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))
