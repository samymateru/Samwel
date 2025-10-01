from fastapi import HTTPException
from psycopg import sql, AsyncConnection
from pydantic import BaseModel
from typing import TypeVar, Optional, Union
from psycopg.types.json import Json

schema_type = TypeVar("schema_type", bound=BaseModel)

class InsertQueryBuilder:
    """
    A utility class for building and executing parameterized SQL INSERT statements
    using an asynchronous PostgreSQL connection (psycopg3) and Pydantic finding_sheet.

    This builder supports:
    - Specifying the target table.
    - Providing insert values via a Pydantic model.
    - Optionally returning specific fields after insertion.
    - Checking for record existence based on one or more columns before inserting.

    Example usage:
        builder = (
            InsertQueryBuilder(connection)
            .into_table("users")
            .values(UserModel(name="Alice", email="alice@example.com"))
            .check_exists({"email": "alice@example.com"})
            .returning("id", "name")
        )
        result = await builder.execute()
    """

    def __init__(self, connection: AsyncConnection):
        """
        Initialize the InsertQueryBuilder.

        Args:
            connection (AsyncConnection): An active asynchronous PostgresSQL connection
                                          (from psycopg3) used for executing the query.
        """
        self.connection: AsyncConnection = connection
        self._table: Optional[str] = None
        self._data: Optional[BaseModel] = None
        self._returning_fields: list[str] = []
        self._check_exists: Optional[dict[str, any]] = None
        self._raw_query: Optional[sql.SQL] = None
        self._raw_params: Optional[dict] = None
        self._throw_error_on_exists: bool = True



    def into_table(self, table: str) -> "InsertQueryBuilder":
        """
        Specify the name of the table into which the data will be inserted.

        Args:
            table (str): The name of the target database table.

        Returns:
            InsertQueryBuilder: The current instance for method chaining.
        """
        self._table = table
        return self


    def raw(self, raw_query: Union[str, sql.SQL], params: dict) -> "InsertQueryBuilder":
        """
        Provide a raw SQL query and parameter dictionary to execute directly.

        Args:
            raw_query (str | sql.SQL): The raw SQL query to be executed.
            params (dict): The parameter dictionary to be used in the query.

        Returns:
            UpdateQueryBuilder: The current instance with raw mode enabled.
        """
        self._raw_query = raw_query
        self._raw_params = params
        return self

    def throw_error_on_exists(self, value: bool) -> "InsertQueryBuilder":
        """Enable throwing an error instead of returning early when a record exists."""
        self._throw_error_on_exists = value
        return self

    def _convert_params(self, params: dict) -> dict:
        """
        Convert unsupported Python types (like dict) into PostgreSQL-compatible types.
        Dicts are wrapped in psycopg's Json for JSONB insertion.
        """
        for k, v in params.items():
            if isinstance(v, dict):
                params[k] = Json(v)
        return params


    def values(self, data: schema_type) -> "InsertQueryBuilder":
        """
        Provide the data to insert using a Pydantic model.

        Args:
            data (schema_type): A Pydantic model instance containing the column-value pairs
                                to be inserted.

        Returns:
            InsertQueryBuilder: The current instance for method chaining.
        """
        self._data = data
        return self


    def returning(self, *fields: str) -> "InsertQueryBuilder":
        """
        Specify one or more fields to return after the insert operation.

        Args:
            *fields (str): One or more column names to return from the inserted row(s).

        Returns:
            InsertQueryBuilder: The current instance for method chaining.
        """
        self._returning_fields.extend(fields)
        return self


    def check_exists(self, conditions: dict[str, any]) -> "InsertQueryBuilder":
        """
        Specify column-value conditions to check whether a matching record already exists
        in the target table before performing the insert.

        If a record exists that satisfies all specified conditions, the insert will be
        skipped, and a message or the existing record (if implemented) will be returned.

        Args:
            conditions (dict[str, any]): A dictionary where keys are column names and values
                                         are the expected values to check for existence.

        Returns:
            InsertQueryBuilder: The current instance for method chaining.

        Example:
            .check_exists({"email": "user@example.com"})
            .check_exists({"id": 5, "name": "Alice"})
        """
        if self._check_exists is None:
            self._check_exists = {}

        self._check_exists.update(conditions)
        return self

    def build(self):
        """
        Construct the SQL INSERT statement and associated parameter values.

        This method uses the table name and data provided via the `into_table()` and `values()`
        methods to generate a parameterized SQL query. If any `returning()` fields were specified,
        a RETURNING clause will be included in the final query.

        Raises:
            ValueError: If the table name or insert data has not been provided.

        Returns:
            tuple:
                - query (psycopg.sql.Composed): A composable SQL query object ready for execution.
                - values (dict): A dictionary of column-value mappings to be used as parameters
                                 in the SQL execution.

        Example:
            query, params = builder.build()
        """
        if not self._table or not self._data:
            raise ValueError("Table and data must be provided.")

        fields = list(self._data.model_fields.keys())
        values = self._data.model_dump()

        columns_sql = sql.SQL(', ').join(map(sql.Identifier, fields))
        placeholders = sql.SQL(', ').join(sql.Placeholder(k) for k in fields)

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
        """
        Execute the INSERT query using the provided connection and data.

        This method performs the following steps:
        1. If `check_exists()` was used, it first checks whether a record with the
           given conditions already exists in the table.
           - If such a record exists, the insert is skipped and a message is returned.
        2. If the record does not exist:
           - Builds and executes the INSERT query with parameterized values.
           - Optionally returns specified fields if `returning()` was used.

        Returns:
            dict | None:
                - If `returning()` fields were specified, returns a dictionary of the inserted row.
                - If a record already exists, returns a message dict with a detail key.
                - If no fields were returned, returns None.

        Raises:
            HTTPException: If the insert fails due to a database error or query execution issue.

        Example:
            result = await builder.execute()
        """


        # Execute raw SQL if specified
        if self._raw_query:
            try:
                async with self.connection.cursor() as cursor:
                    await cursor.execute(self._raw_query, self._raw_params)

                    if self._returning_fields:
                        row = await cursor.fetchone()
                        if row:
                            column_names = [desc[0] for desc in cursor.description]
                            return dict(zip(column_names, row))
                    return None
            except Exception as e:
                raise Exception(f"Failed to execute raw SQL: {e}")

        if self._check_exists:
            where_clause = sql.SQL(" AND ").join(
                sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder(k))
                for k in self._check_exists.keys()
            )
            # Instead of SELECT 1, select all columns
            exists_query = sql.SQL("SELECT * FROM {} WHERE {} LIMIT 1").format(
                sql.Identifier(self._table),
                where_clause
            )

            try:
                async with self.connection.cursor() as cursor:
                    await cursor.execute(exists_query, self._check_exists)
                    row = await cursor.fetchone()
                    if row:
                        if self._throw_error_on_exists:
                            raise HTTPException(
                                status_code=409,
                                detail=f"Record already exists in {self._table.replace('Tables', '')}"
                            )
                        # ✅ Return existing record as dict
                        col_names = [desc.name for desc in cursor.description]
                        result = dict(zip(col_names, row))
                        result["exists"] = True
                        return result

            except HTTPException:
                raise
            except Exception as e:
                raise Exception(f"Failed to check record existence: {e}")

        query, params = self.build()
        params = self._convert_params(params)
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
            raise Exception(f"""Failed to insert record in table {self._table.replace('_', ' ')
            .title() if '_' in self._table else self._table.capitalize()} due to error: {e}""")




