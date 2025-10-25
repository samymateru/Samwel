from fastapi import Depends
from services.connections.postgres.connections import get_asyncpg_db_connection, DBConnection
from utils import exception_response


async def manage_staff_limits(connection: DBConnection = Depends(get_asyncpg_db_connection)):
    with exception_response():
        pass