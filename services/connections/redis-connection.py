from redis.asyncio import Redis, ConnectionPool
from typing import AsyncGenerator

redis_pool: ConnectionPool = ConnectionPool.from_url(
    "redis://localhost:6379",
    max_connections=20,
    decode_responses=True
)

redis_client: Redis = Redis(connection_pool=redis_pool)

async def get_redis() -> AsyncGenerator[Redis, None]:
    yield redis_client




import json
from functools import wraps
from typing import Callable, Awaitable

def redis_cache(key_builder: Callable[..., str], expire: int = 60):
    def decorator(func: Callable[..., Awaitable]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis: Redis = kwargs.get("redis")  # expect redis to be passed
            key = key_builder(*args, **kwargs)

            if redis is None:
                return await func(*args, **kwargs)

            # Try to get from Redis
            cached = await redis.get(key)
            if cached:
                return json.loads(cached)

            # Call original function
            result = await func(*args, **kwargs)

            # Cache the result
            await redis.set(key, json.dumps(result), ex=expire)
            return result

        return wrapper
    return decorator


#
# @redis_cache(
#     key_builder=lambda user_id, include_sensitive=False, **_: f"user:{user_id}:sensitive:{include_sensitive}"
# )