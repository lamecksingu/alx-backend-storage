#!/usr/bin/env python3
""" Implementation of top_students function """


def top_students(mongo_collection):
    """ Return all the students sorted by average score """
    return mongo_collection.aggregate([
        {'$project': {
            'name': '$name',
            'averageScore': {'$avg': '$topics.score'}
        }
        },
        {'$sort': {'averageScore': -1}}
    ])
