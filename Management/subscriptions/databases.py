from psycopg import AsyncConnection

from services.connections.query_builder import ReadBuilder
from utils import exception_response


async def get_subscription(connection: AsyncConnection):
    with exception_response():
        pass