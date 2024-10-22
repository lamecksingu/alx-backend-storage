#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB

Sample output:

```
94778 logs
Methods:
    method GET: 93842
    method POST: 229
    method PUT: 0
    method PATCH: 0
    method DELETE: 0
47415 status check
```

"""


if __name__ == '__main__':
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    # Display total of documents
    print(nginx.count_documents({}), 'logs')

    # Methods stats
    print('Methods:')

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    for method in methods:
        method_count = nginx.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, method_count))

    # Status check
    status_check_count = nginx.count_documents({'method': 'GET',
                                                'path': '/status'})
    print('{} status check'.format(status_check_count))
