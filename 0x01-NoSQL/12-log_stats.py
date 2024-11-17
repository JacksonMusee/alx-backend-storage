#!/usr/bin/env python3
'''
Write a Python script that provides some stats about Nginx logs
stored in MongoDB:
'''

if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs

    total_logs = db.nginx.count_documents({})

    print(f"{total_logs} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = db.nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_check_count = db.nginx.count_documents(
        {"method": "GET", "path": "/status"})

    print(f"{status_check_count} status check")
