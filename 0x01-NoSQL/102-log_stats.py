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
IPs:
    172.31.63.67: 15805
    172.31.2.14: 15805
    172.31.29.194: 15805
    69.162.124.230: 529
    64.124.26.109: 408
    64.62.224.29: 217
    34.207.121.61: 183
    47.88.100.4: 166
    45.249.84.250: 160
    216.244.66.228: 150
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

    # Top 10 of the most present IPs
    print('IPs:')
    pipeline = [
        {'$group':
            {
                '_id': '$ip',
                'count': {'$sum': 1}
            }
         },
        {'$sort':
            {'count': -1}
         },
        {'$limit': 10}
    ]
    ip_count = nginx.aggregate(pipeline)

    for ip in ip_count:
        print(f'\t{ip.get("_id")}: {ip.get("count")}')
