import json
import os
from typing import Optional
import asyncpg
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

from asyncpg import Connection


DBConnection = Connection

load_dotenv()



class AsyncDBPoolSingleton:
    """
    Singleton class that manages a single instance of an asynchronous PostgresSQL connection pool.

    This class ensures that only one `AsyncConnectionPool` instance exists across the application,
    allowing efficient reuse of database connections. The connection pool is lazily initialized
    when first accessed via `get_pool()`.

    Environment variables required:
        - DB_USER: Database username
        - DB_PASSWORD: Database password
        - DB_HOST: Database host
        - DB_PORT: Database port
        - DB_NAME: Database name
    """

    _instance = None

    def __init__(self):
        """
        Initialize the singleton instance. The actual connection pool is not created until
        `get_pool()` is called.
        """
        self._pool: Optional[AsyncConnectionPool] = None

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the AsyncDBPoolSingleton.

        Returns:
            AsyncDBPoolSingleton: The singleton instance of the connection pool manager.
        """
        if cls._instance is None:
            cls._instance = AsyncDBPoolSingleton()
        return cls._instance

    async def get_pool(self):
        """
        Get or initialize the asynchronous PostgresSQL connection pool.

        If the connection pool has not been created yet, this method initializes it
        using environment variables for configuration. Otherwise, it returns the existing pool.

        Returns:
            AsyncConnectionPool: The active asynchronous connection pool.
        """
        if self._pool is None:
            self._pool = AsyncConnectionPool(
                conninfo=(
                    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
                    f"?application_name=fastapi-app"
                ),
                min_size=10,
                max_size=100,
                open=False,  # Prevent automatic opening; open manually.
            )
            await self._pool.open()
        return self._pool

    async def close_pool(self):
        """
        Close the async PostgresSQL connection pool if it has been initialized.

        This method safely closes the connection pool and releases all active
        database connections. It should be called during application shutdown
        to ensure graceful cleanup of resources.

        Example usage:
            await AsyncDBPoolSingleton.get_instance().close_pool()
        """
        if self._pool:
            await self._pool.close()

    @staticmethod
    async def get_db_connection():
        pool = await AsyncDBPoolSingleton.get_instance().get_pool()
        async with pool.connection() as conn:
            yield conn




class AsyncPGPoolSingleton:
    """
    Singleton class that manages a single instance of an asyncpg connection pool.

    All connections are eagerly initialized (not lazy), so the pool is ready
    immediately after creation.

    Environment variables required:
        - DB_USER
        - DB_PASSWORD
        - DB_HOST
        - DB_PORT
        - DB_NAME
    """

    _instance = None

    def __init__(self):
        self._pool: asyncpg.pool.Pool | None = None


    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = AsyncPGPoolSingleton()
            await cls._instance._initialize_pool()
        return cls._instance


    @staticmethod
    async def _register_codecs(conn: asyncpg.Connection):
        """Register JSON/JSONB codecs on a connection."""
        await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog',
        )

        await conn.set_type_codec(
            'jsonb',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog',
        )



    async def _initialize_pool(self):
        """Create the asyncpg pool and initialize all connections eagerly."""
        self._pool = await asyncpg.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 5432)),
            min_size=10,  # Minimum connections
            max_size=50,  # Maximum connections
            init=self._register_codecs
        )



    async def close_pool(self):
        """Close the connection pool."""
        if self._pool:
            await self._pool.close()


    async def get_db_connection(self):
        """Async generator to yield a connection from the pool."""
        async with self._pool.acquire() as conn:
            yield conn



async def get_db_connection():
    pool = await AsyncDBPoolSingleton.get_instance().get_pool()
    async with pool.connection() as conn:
        yield conn


async def get_asyncpg_db_connection():
    pool_singleton = await AsyncPGPoolSingleton.get_instance()
    async for conn in pool_singleton.get_db_connection():
        yield conn
