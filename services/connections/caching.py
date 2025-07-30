import json
from typing import Callable, Awaitable

from fastapi import HTTPException

from core.encoders import DateTimeEncoder
from functools import wraps

from services.connections.redis_connection import get_redis


def cache(identifier: str, expire: int = 60):
    """
    Cache decorator that accepts the `param_name` (e.g., 'engagement_id') and caches the result
    based on that parameter.
    """

    def decorator(func: Callable[..., Awaitable]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = kwargs.get(identifier)

            if key is None:
                raise HTTPException(status_code=400, detail="Missing function kwargs")

            async for redis in get_redis():
                if redis:
                    cached = await redis.get(key)
                    if cached:
                        return json.loads(cached)  # Return cached data

                # If no cache, call the original function
                result = await func(*args, **kwargs)

                # If Redis is available, cache the result
                if redis:
                    await redis.set(key, json.dumps(result, cls=DateTimeEncoder), ex=expire)

                return result

        return wrapper

    return decorator