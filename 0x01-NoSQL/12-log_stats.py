#!/usr/bin/env python3

from pymongo import MongoClient


def log_stats():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Number of documents in the collection
    total_logs = collection.count_documents({})

    # Methods count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
        {"method": method}) for method in methods}

    # Count for specific method and path
    specific_count = collection.count_documents(
        {"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")

    print(f"{specific_count} status check")


if __name__ == "__main__":
    log_stats()
