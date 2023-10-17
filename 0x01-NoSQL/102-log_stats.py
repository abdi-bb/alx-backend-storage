#!/usr/bin/env python3
'''
Module: '102-log_stats'
'''


from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Provide statistics about Nginx logs stored in a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection of Nginx logs.

    Returns:
        dict: A dictionary containing log statistics.
    """
    # Count the total number of logs
    total_logs = mongo_collection.count_documents({})

    # Count the number of logs for each HTTP method
    methods = [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
    method_counts = {}
    for method in methods:
        method_counts[method] = mongo_collection.count_documents({"method": method})

    # Count the number of logs with method=GET and path=/status
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})

    # Count the number of logs for each IP and sort them in descending order
    ip_counts = {}
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    for doc in mongo_collection.aggregate(pipeline):
        ip_counts[doc["_id"]] = doc["count"]

    return {
        "Total Logs": total_logs,
        "Methods": method_counts,
        "Status Check": status_check_count,
        "IPs": ip_counts
    }

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    stats = log_stats(logs_collection)
    print(f"{stats['Total Logs']} logs")
    print("Methods:")
    for method, count in stats['Methods'].items():
        print(f"    method {method}: {count}")
    print(f"{stats['Status Check']} status check")
    print("IPs:")
    for ip, count in stats['IPs'].items():
        print(f"    {ip}: {count}")
