import hashlib
import json
import pickle
from functools import wraps
from fastapi import HTTPException

import asyncio
import redis.asyncio as redis
from redis.asyncio import Redis
from typing import Optional

redis_queue: Optional[asyncio.Queue] = None
redis_client: Optional[Redis] = None
REDIS_POOL_SIZE = 100

def safe_serialize(obj):
    try:
        return json.dumps(obj, sort_keys=True)
    except TypeError:
        return str(obj)

def cached(ttl: int = 300, prefix: str = "cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            global redis_client
            try:
                redis_client = await get_redis_connection()
                key_raw = json.dumps({
                    "func": func.__name__,
                    "args": [safe_serialize(arg) for arg in args],
                    "kwargs": {k: safe_serialize(v) for k, v in kwargs.items() if k != "connection"}
                }, sort_keys=True)
                key = f"{prefix}:{hashlib.sha256(key_raw.encode()).hexdigest()}"

                # Check Redis cache first
                cached_data = await redis_client.get(key)
                if cached_data: # Cache hit return the data
                    await return_redis_connection(redis_client)
                    return pickle.loads(cached_data)

                else:# Cache miss, execute the actual function
                    result = await func(*args, **kwargs)
                    await redis_client.set(key, pickle.dumps(result), ex=ttl)
                    await return_redis_connection(redis_client)
                    return result
            except RuntimeError:
                await return_redis_connection(redis_client)
                result = await func(*args, **kwargs)
                return result
            except HTTPException as e:
                await return_redis_connection(redis_client)
                raise  HTTPException(status_code=e.status_code, detail=e.detail)
        return wrapper
    return decorator

async def create_redis_connection() -> Redis:
    return redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=False
    )

async def init_redis_pool():
    global redis_queue
    redis_queue = asyncio.Queue(maxsize=REDIS_POOL_SIZE)

    for _ in range(REDIS_POOL_SIZE):
        conn = await create_redis_connection()
        await redis_queue.put(conn)

async def get_redis_connection() -> Redis:
    if redis_queue is None:
        raise RuntimeError("Redis pool not initialized")
    try:
        return await asyncio.wait_for(redis_queue.get(), timeout=2)
    except asyncio.TimeoutError:
        raise RuntimeError("Time out")

async def return_redis_connection(conn: Redis):
    if redis_queue is None:
        raise RuntimeError("Redis pool not initialized")
    await redis_queue.put(conn)

async def close_redis_pool():
    if redis_queue:
        while not redis_queue.empty():
            conn: Redis = await redis_queue.get()
            await conn.close()