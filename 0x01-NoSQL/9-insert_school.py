#!/usr/bin/env python3
""" Implementation of insert_school function """


def insert_school(mongo_collection, **kwargs):
    """ Insert a new document in a collection based on kwargs """
    insert_result = mongo_collection.insert_one(kwargs)
    return insert_result.inserted_id
