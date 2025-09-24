from psycopg import AsyncConnection
from typing import Dict
from utils import exception_response


async def add_library_item(connection: AsyncConnection, module_id: str):
    with exception_response():
        pass
