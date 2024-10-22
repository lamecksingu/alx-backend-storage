#!/usr/bin/env python3
""" Implementation of schools_by_topic function """


def schools_by_topic(mongo_collection, topic):
    """ Return the list of school having a specific topic """
    return mongo_collection.find({'topics': {'$in': [topic]}})
