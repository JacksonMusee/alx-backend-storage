#!/usr/bin/env python3
'''
Improve 12-log_stats.py by adding the top 10 of the most present IPs in the collection nginx of the database logs:

    The IPs top must be sorted.
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

    print("IPS:")
    ip_records = {}
    for log in db.nginx.find({}):
        ip = log["ip"]
        if ip in ip_records:
            ip_records["ip"] += 1
        else:
            ip_records["ip"] = 1

    sorted_ip_records = sorted(
        ip_records.items(), key=lambda x: x[1], reverse=True)

    for i in range(10):
        try:
            for key, value in sorted_ip_records[i]:
                print(f"\t{key}: {value}")
        except Exception as e:
            exit
