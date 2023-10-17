#!/usr/bin/env python3
'''
Module: '8-all'
'''


def list_all(mongo_collection):
    """Lists all documents in a MongoDB collection."""
    return [doc for doc in mongo_collection.find()]
