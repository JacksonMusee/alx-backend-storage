#!/usr/bin/env python3
'''
Write a Python function that returns all students sorted by average score:

    Prototype: def top_students(mongo_collection):
    mongo_collection will be the pymongo collection object
    The top must be ordered
    The average score must be part of each item returns with key = averageScore
'''


def top_students(mongo_collection):
    '''
    Does as required above
    '''
    students = mongo_collection.find({})
    students_with_avscore = []

    for student in students:
        avscore = sum(score["score"]
                      for score in student["topics"]) / len(student["topics"])
        student["averageScore"] = avscore
        students_with_avscore.append(student)

    return sorted(students_with_avscore(key=lambda x: x["averageScore"], reverse=True))
