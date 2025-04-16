import hashlib
import json
from functools import wraps
from typing import Callable, Any, Awaitable

from psycopg2.extensions import connection as Connection
from redis_client import redis_client  # assumes aioredis or redis.asyncio

from Management.companies.databases import get_companies


def cached(ttl: int = 300, prefix: str = "cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_raw = json.dumps({
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs
            }, sort_keys=True)
            key = f"{prefix}:{hashlib.sha256(key_raw.encode()).hexdigest()}"

            # Check Redis cache first
            cached_data = await redis_client.get(key)
            if cached_data:
                print("✅ Cache hit")
                return json.loads(cached_data)

            # Cache miss, execute the actual function
            try:
                print("❌ Cache miss — executing function")
                result = await func(*args, **kwargs)

                # If function was successful, cache the result
                await redis_client.set(key, json.dumps(result), ex=ttl)
                print("📦 Cached result to Redis")
                return result
            except Exception as e:
                print(f"⚠️ Error occurred: {e}")
                raise  # Reraise the exception to propagate the error
        return wrapper
    return decorator



@cached(ttl=300)
async def get_data(key: str, connection: Connection):
    data = get_companies(connection=connection, company_id=1)
    return data

