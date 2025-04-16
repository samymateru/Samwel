
from functools import wraps
import hashlib
import json

from watchfiles import awatch


def cached(ttl: int = 60, prefix: str = "cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_raw = json.dumps({"func": func.__name__, "args": args, "kwargs": kwargs}, sort_keys=True)
            key = f"{prefix}:{hashlib.sha256(key_raw.encode()).hexdigest()}"
            print(key_raw)
            result = ""
            return result

        return wrapper
    return decorator

@cached(ttl=100)
async def data(param: str):
    return "sam"


import asyncio

asyncio.run(data("sam"))
