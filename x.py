import sys
from psycopg_pool import AsyncConnectionPool
import os
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from dotenv import load_dotenv
load_dotenv()
# Ensure you load the .env or environment variables before starting.
# Make sure that DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME are set properly.

# Async context manager for database connection
async def get_db_connection_async():
    # Ensure the pool is created and opened properly
    connection_pool_async = AsyncConnectionPool(
        conninfo=f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
        min_size=1,
        max_size=10,
        open=False,  # IMPORTANT: prevent auto-opening
    )
    print(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",)
    try:
        await connection_pool_async.open()  # Manually open it
        async with connection_pool_async.connection() as conn:
            yield conn
    except Exception as e:
        print(f"Error getting DB connection: {e}")
    finally:
        await connection_pool_async.close()  # Close the pool after usage to free resources.


# Wrapper function to use the connection pool
async def get_async_db_connection():
    async with get_db_connection_async() as conn:
        # Perform database operations
        return conn  # You can return the connection to use in further async queries.


# Example async function that will use the database connection
async def perform_db_operations():
    async for conn in get_db_connection_async():
        # Perform some operations using conn (which is a database connection object)
        print(conn)


# Run the operations
asyncio.run(perform_db_operations())
