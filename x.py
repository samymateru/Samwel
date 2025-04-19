from psycopg2.extensions import connection as Connection
from typing import List
from utils  import get_db_connection

tb = [
    "engagements"
]


def update(connection: Connection, tables: List[str]):
    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute(f"ALTER TABLE {table} ALTER COLUMN id DROP DEFAULT;")
            cursor.execute(f"ALTER TABLE {table} ALTER COLUMN id TYPE VARCHAR;")
            connection.commit()

con = next(get_db_connection())

update(connection=con, tables=tb)
