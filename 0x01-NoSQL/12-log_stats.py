#!/usr/bin/env python3
'''
Write a Python script that provides some stats about Nginx logs
stored in MongoDB:
'''

from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.logs

total_logs = db.nginx.count_documents({})

print(f"{total_logs} logs")

print("Methods:")
for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
    count = db.nginx.count({"method": method})
    print(f"\tmethod {method}: {count}")
