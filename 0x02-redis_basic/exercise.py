#!/usr/bin/env python3
'''
Create a Cache class. In the __init__ method, store an instance of the
Redis client as a private variable named _redis (using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes, int or float.
'''
import uuid
import redis
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Decorator to count the number of times a method is called.
    Increments a Redis counter using the method's qualified name.
    '''
    @ wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    A decorator to store the history of inputs and outputs for a method.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"

        self._redis.rpush(key_inputs, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(key_outputs, str(result))

        return result

    return wrapper


class Cache:
    '''
    AS above
    '''

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Does as required above
        '''
        my_key = str(uuid.uuid4())
        self._redis.set(my_key, data)
        return my_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        '''
        TakeS a key string argument and an optional Callable argument named fn.
        This callable will be used to convert the data back to the desired format.
        '''
        value = self._redis.get(key)
        if value is None:
            return None

        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> Optional[str]:
        '''
        Gets a value and return it as string
        '''
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        '''
        Gets a value and return it as int
        '''
        return self.get(key, fn=lambda x: int(x))


def replay(method):
    '''
    Function to display the history of calls for a particular method.
    '''
    key_inputs = f"{method.__qualname__}:inputs"
    key_outputs = f"{method.__qualname__}:outputs"

    # Retrieve the inputs and outputs from Redis
    inputs = cache._redis.lrange(key_inputs, 0, -1)
    outputs = cache._redis.lrange(key_outputs, 0, -1)

    # Print the call history
    print(f"{method.__qualname__} was called {len(inputs)} times:")

    # Combine inputs and outputs using zip, then display them
    for inp, out in zip(inputs, outputs):
        # Convert the input and output back from str to their original format
        # Use eval to turn the string representation back into a tuple
        inp = eval(inp)
        out = out.decode('utf-8')  # Decode bytes to string

        print(f"{method.__qualname__}(*{inp}) -> {out}")
