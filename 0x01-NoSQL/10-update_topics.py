#!/usr/bin/env python3
'''
Module: '10-update_topics
'''


def update_topics(mongo_collection, name, topics):
    '''function that changes all topics of a school document based on the name.'''
    for topic in topics:
        return mongo_collection.update_many({'name': name}, {'$set': {'topic': topics}})
