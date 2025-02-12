#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient

def log_stats():
    """ log_stats function to print log statistics from MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    total = logs_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: logs_collection.count_documents({"method": method}) for method in methods}
    path_count = logs_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{total} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{path_count} status check")
    print("IPs:")
    sorted_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip_doc in sorted_ips:
        print(f"\t{ip_doc['_id']}: {ip_doc['count']}")

if __name__ == "__main__":
    log_stats()
