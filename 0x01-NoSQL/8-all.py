#!/usr/bin/env python3
""" Implementation of list_all function """


def list_all(mongo_collection):
    """ List all the documents of a collection """
    return list(mongo_collection.find())
