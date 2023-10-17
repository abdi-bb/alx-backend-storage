#!/usr/bin/env python3

from pymongo import MongoClient


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection to list documents from.

    Returns:
        list: A list of documents.
    """
    return [doc for doc in mongo_collection.find()]
