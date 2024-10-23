#!/usr/bin/env python3
""" Implement the Cache class """
from functools import wraps
import redis
from typing import Any, Callable, Union
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """ Decorator for store method that increments the count
    for the __qualname__ key every time the method is called

    Return the value returned by the original method
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """

        # Define key
        key = method.__qualname__

        # Increment by one the number of calls
        self.incr(key)

        # Call the store method and return its returned key
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of
    inputs and outputs for a particular function (Cache.store)
    """

    # Define inputs and outputs lists keys
    inputs_key = method.__qualname__ + ':inputs'
    outputs_key = method.__qualname__ + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """

        # Store the inputs
        self.rpush(inputs_key, str(args))

        # Call the method and store the output
        outs = method(self, *args, **kwargs)
        self.rpush(outputs_key, outs)

        # Return the original output
        return outs

    # Return the wrapper
    return wrapper


def replay(method: Callable) -> None:
    """ Display the history of calls of a particular function

    Output example:

    >>> cache = Cache()
    >>> cache.store("foo")
    >>> cache.store("bar")
    >>> cache.store(42)
    >>> replay(cache.store)
    Cache.store was called 3 times:
    Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
    Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
    Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
    """

    # Initialize the history log to be returned
    history_log = ''

    # Make a redis instance
    r = redis.Redis()

    # Construct keys
    fn_key = method.__qualname__
    inputs_key = method.__qualname__ + ':inputs'
    outputs_key = method.__qualname__ + ':outputs'

    # Retrieve count of calls
    count = r.get(fn_key)

    if not count:
        print(f'{fn_key} was called 0 times')

    # Add it to log
    history_log += f'{fn_key} was called {int(count)} times:\n'

    # Retrieve inputs and outputs
    inputs = r.lrange(inputs_key, 0, -1)
    outputs = r.lrange(outputs_key, 0, -1)

    # Update history_log while iterating through zipped inputs and outputs
    for inp, outp in zip(inputs, outputs):
        history_log += f'{fn_key}(*{inp.decode()}) -> {outp.decode()}\n'

    # Print the history log
    print(history_log, end='')


class Cache:
    """ Encapsulate some Redis features """

    def __init__(self) -> None:
        """ Instantiate a Redis client and flush it """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key, store the input data in
        Redis using the random key and return the key
        """

        # Generate the key using uuid4
        key = str(uuid4())

        # Store it in the Redis database
        self._redis.set(key, data)

        # Return the key
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
        """ Take a key string argument and return the stored value if any """

        # Retrieve value
        value = self._redis.get(key)

        # Format with `fn` if relevant
        if value and fn:
            value = fn(value)

        # Return the value
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """ Get and return the string value stored in key """
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """ Get and return the integer value stored in key """
        return self.get(key, int)

    def set(self, key: str, value: Union[str, bytes, int, float]) -> None:
        """ Set a key-value pair """
        self._redis.set(key, value)

    def incr(self, key: str) -> None:
        """ Increment the stored value in that key by 1 """
        self._redis.incr(key)

    def rpush(self, key: str, value: Union[str, bytes, int, float]) -> None:
        """ Right push the value to the list stored in that key """
        self._redis.rpush(key, value)
