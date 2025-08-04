from fastapi import HTTPException
from psycopg import sql, AsyncConnection
from pydantic import BaseModel
from typing import TypeVar, Optional

schema_type = TypeVar("schema_type", bound=BaseModel)

class InsertQueryBuilder:
    def __init__(self, connection: AsyncConnection):
        self.connection: AsyncConnection = connection
        self._table: Optional[str] = None
        self._data: Optional[BaseModel] = None
        self._returning_fields: list[str] = []

    def into_table(self, table: str) -> "InsertQueryBuilder":
        self._table = table
        return self

    def values(self, data: schema_type) -> "InsertQueryBuilder":
        self._data = data
        return self

    def returning(self, *fields: str) -> "InsertQueryBuilder":
        self._returning_fields.extend(fields)
        return self

    def build(self):
        if not self._table or not self._data:
            raise ValueError("Table and data must be provided.")

        fields = list(self._data.model_fields.keys())
        values = self._data.model_dump()

        columns_sql = sql.SQL(', ').join(map(sql.Identifier, fields))
        placeholders = sql.SQL(', ').join(
            sql.Placeholder(k) for k in fields
        )

        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(self._table),
            columns_sql,
            placeholders
        )

        if self._returning_fields:
            returning_sql = sql.SQL(', ').join(map(sql.Identifier, self._returning_fields))
            query += sql.SQL(" RETURNING ") + returning_sql

        return query, values

    async def execute(self):
        query, params = self.build()
        try:
            async with self.connection.cursor() as cursor:
                await cursor.execute(query, params)

                if self._returning_fields:
                    row = await cursor.fetchone()
                    if row is not None:
                        column_names = [desc[0] for desc in cursor.description]
                        return dict(zip(column_names, row))
                return None

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Insert failed: {e}")


