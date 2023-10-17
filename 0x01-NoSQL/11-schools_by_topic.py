#!/usr/bin/env python3
'''
Module: '11-schools_by_topic'
'''


def schools_by_topic(mongo_collection, topic):
    '''Returns the list of docs having specific topic'''
    return list(mongo_collection.find({'topic': topic}))
