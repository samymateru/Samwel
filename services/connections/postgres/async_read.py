from fastapi import HTTPException
from psycopg import sql
from asyncpg import Connection
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel

schema_type = TypeVar("schema_type", bound=BaseModel)

class ReadBuilder:
    def __init__(self, connection: Connection = None):
        self.connection: Connection = connection
        self._order_by_fields = []
        self._group_by_fields = []
        self._select = []
        self._table = None
        self._where = []
        self._order_by = None
        self._order_desc = False
        self._limit = None
        self._offset = None
        self._params = []
        self._joins = []
        self._table_alias = None
        self._distinct = False

    def distinct(self, *columns: str):
        """
        If called with no arguments:
            .distinct() -> SELECT DISTINCT
        If called with arguments:
            .distinct("iss.id") -> SELECT DISTINCT ON (iss.id)
        """
        if columns:
            self._distinct = columns  # store the list
        else:
            self._distinct = True
        return self

    def join(self, join_type: str, table: str, on: str, alias: Optional[str] = None,
             model: Optional[Type[BaseModel]] = None, use_prefix: bool = True):
        join_clause = {
            "type": join_type.upper(),
            "table": table,
            "alias": alias,
            "on": on,
            "model": model,
            "use_prefix": use_prefix  # NEW!
        }
        self._joins.append(join_clause)
        return self

    def select_joins(self):
        for join in self._joins:
            model = join.get("model")
            alias = join.get("alias")
            use_prefix = join.get("use_prefix", True)

            if model and alias:
                for field in model.model_fields.keys():
                    field_path = f"{alias}.{field}"
                    alias_name = f"{alias}_{field}" if use_prefix else field
                    self._select.append((field_path, alias_name))
        return self

    def build_group_by_clause(self):
        if self._group_by_fields:
            identifiers = []
            for col in self._group_by_fields:
                if "." in col:
                    table_alias, column_name = col.split(".", 1)
                    identifiers.append(
                        sql.SQL("{}.{}").format(sql.Identifier(table_alias), sql.Identifier(column_name))
                    )
                else:
                    identifiers.append(sql.Identifier(col))
            return sql.SQL(" GROUP BY ") + sql.SQL(", ").join(identifiers)
        return sql.SQL("")

    def select(self, columns: Type[schema_type]):
        # Store field names as (field, None) to match the expected format
        self._select = [(field, None) for field in columns.model_fields.keys()]
        return self


    def select_fields(self, *fields: str, alias_map: Optional[dict[str, str]] = None):
        alias_map = alias_map or {}
        for field in fields:
            alias = alias_map.get(field)
            self._select.append((field, alias))
        return self


    def from_table(self, table: str, alias: Optional[str] = None):
        self._table = table
        self._table_alias = alias
        return self


    def where(self, column: str, value):
        if column is None:
            raise ValueError("Column can't be None")

        # Determine if value is a list/tuple/set
        if isinstance(value, (list, tuple, set)):
            # Store the value as a list for asyncpg
            self._params = getattr(self, "_param_values", [])
            param_index = len(self._params) + 1
            self._params.append(list(value))  # asyncpg supports ANY($1)
            condition = f"{column} = ANY(${param_index})"
        else:
            self._params = getattr(self, "_param_values", [])
            param_index = len(self._params) + 1
            self._params.append(value)
            condition = f"{column} = ${param_index}"

        self._where.append(condition)
        return self


    def where_raw(self, condition: str, params: Optional[dict] = None):
        """
        Add a raw WHERE condition with optional bound parameters.
        Example:
            where_raw("next_reference <= NOW()")
            where_raw("next_reference <= %(end_time)s", {"end_time": some_datetime})
        """
        self._where.append(condition)
        if params:
            pass
        return self


    def order_by(self, column: str, descending=False):
        if column is None:
            raise ValueError("Value of column can't be None")

        self._order_by_fields.append((column, descending))
        return self


    def group_by(self, column: str):
        if column is None:
            raise ValueError("Group by column can't be None")
        self._group_by_fields.append(column)
        return self

    def limit(self, count: int):
        self._limit = count
        return self

    def offset(self, count: int):
        self._offset = count
        return self


    def build(self):
        if not self._table:
            raise ValueError("Table name cannot be empty")

        if not self._select:
            select_clause = sql.SQL("*")
        else:
            select_parts = []
            for col, alias in self._select:
                if isinstance(col, sql.Composable):
                    if alias:
                        select_parts.append(sql.SQL("{} AS {}").format(col, sql.Identifier(alias)))
                    else:
                        select_parts.append(col)
                else:
                    # Handle strings / identifiers as before
                    if "." in col:
                        table_alias, column_name = col.split(".", 1)
                        column_sql = sql.SQL("{}.{}").format(
                            sql.Identifier(table_alias), sql.Identifier(column_name)
                        )
                    else:
                        if self._table_alias:
                            column_sql = sql.SQL("{}.{}").format(
                                sql.Identifier(self._table_alias), sql.Identifier(col)
                            )
                        else:
                            column_sql = sql.Identifier(col)

                    if alias:
                        select_parts.append(
                            sql.SQL("{} AS {}").format(column_sql, sql.Identifier(alias))
                        )
                    else:
                        select_parts.append(column_sql)

            select_clause = sql.SQL(", ").join(select_parts)

        from_clause = sql.SQL("FROM {}").format(sql.SQL("{} AS {}").format(sql.Identifier(self._table), sql.Identifier(self._table_alias)) if self._table_alias else sql.Identifier(self._table))

        # Add JOINs
        join_clauses = []
        for join in self._joins:
            join_type = sql.SQL(join["type"] + " JOIN")
            table_id = sql.Identifier(join["table"])
            alias = sql.Identifier(join["alias"]) if join["alias"] else None
            on_clause = sql.SQL(join["on"])  # Keep raw string — if safe
            alias_sql = sql.SQL("AS ") + alias if alias else sql.SQL("")
            join_clause = sql.SQL(" {} {} {} ON {}").format(
                join_type,
                table_id,
                alias_sql,
                on_clause
            )
            join_clauses.append(join_clause)


        if isinstance(self._distinct, (tuple, list)):
            distinct_cols = [sql.SQL(col) for col in self._distinct]
            select_prefix = (
                    sql.SQL("SELECT DISTINCT ON (") +
                    sql.SQL(", ").join(distinct_cols) +
                    sql.SQL(") ")
            )
        elif self._distinct is True:
            select_prefix = sql.SQL("SELECT DISTINCT ")
        else:
            select_prefix = sql.SQL("SELECT ")

        query = select_prefix + select_clause + sql.SQL(" ") + from_clause + sql.SQL("").join(join_clauses)

        if self._where:
            where_clause = sql.SQL(" WHERE ") + sql.SQL(" AND ").join(
                sql.SQL(cond) for cond in self._where
            )
            query += where_clause

        if self._group_by_fields:
            query += self.build_group_by_clause()

        if self._order_by_fields:
            order_clauses = []
            for column, descending in self._order_by_fields:
                direction = sql.SQL("DESC") if descending else sql.SQL("ASC")
                order_clauses.append(
                    sql.SQL("{} {}").format(sql.Identifier(column), direction)
                )
            query += sql.SQL(" ORDER BY ") + sql.SQL(", ").join(order_clauses)

        if self._limit is not None:
            query += sql.SQL(" LIMIT $(limit)s")


        if self._offset is not None:
            query += sql.SQL(" OFFSET $(offset)s")


        return query, self._params


    async def fetch_all(self):
        query, param = self.build()
        try:
            rows = await self.connection.fetch(query.as_string(), *param)
            return [dict(row) for row in rows]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error occurred while fetching data: {e}")


    def join_aggregate(
        self,
        table: str,
        alias: str,
        on: str,
        aggregate_column: str,
        json_field_name: str,
        model: Optional[Type[BaseModel]] = None,
        use_prefix: bool = True,
        filter_condition: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        join_type: str = "LEFT",
        as_object: bool = False
    ):
        """
        Adds a LEFT JOIN with JSON aggregation.
        Example:
            .join_aggregate(
                table="engagements",
                alias="eng",
                on="ap.id = eng.plan_id",
                aggregate_column="id",
                json_field_name="engagements",
                model=ReadEngagement
            )
        """
        # --- Build jsonb_build_object(...) ---
        if model:
            fields_sql = []
            for field_name in model.model_fields.keys():
                col_ref = (
                    sql.SQL("{}.{}").format(sql.Identifier(alias), sql.Identifier(field_name))
                    if use_prefix
                    else sql.Identifier(field_name)
                )

                fields_sql.append(sql.SQL("{} , {}").format(sql.Literal(field_name), col_ref))

            json_object = sql.SQL("jsonb_build_object({})").format(
                sql.SQL(", ").join(fields_sql)
            )

        else:
            json_object = sql.SQL("{}.{}").format(
                sql.Identifier(alias),
                sql.Identifier(aggregate_column)
            )


        if filter_condition:
            filter_sql = self.build_filter_sql(filter_condition) # type: ignore[arg-type]
        else:
            alias_col = sql.SQL("{}.{}").format(
                sql.Identifier(alias),
                sql.Identifier(aggregate_column)
            )
            filter_sql = sql.SQL("{} IS NOT NULL").format(alias_col)

        subquery_parts = [
            sql.SQL("SELECT {json_obj}").format(json_obj=json_object),
            sql.SQL("FROM {table} {alias}").format(
                table=sql.Identifier(table),
                alias=sql.Identifier(alias)
            ),
            sql.SQL("WHERE {on} AND {filter_sql}").format(
                on=sql.SQL(on), # type: ignore[arg-type]
                filter_sql=filter_sql
            ),
        ]

        if order_by:
            subquery_parts.append(sql.SQL(f"ORDER BY {order_by}")) # type: ignore[arg-type]
        if limit:
            subquery_parts.append(sql.SQL(f"LIMIT {limit}")) # type: ignore[arg-type]

        subquery = sql.SQL(" ").join(subquery_parts)

        # --- Step 4: JSON aggregation of subquery (no wrapper key) ---
        if as_object:
            # 🔸 Return a single JSON object (first element or empty)
            json_agg = sql.SQL(
                 "(SELECT jsonb_agg(subq.elem)->0 FROM ({subquery}) AS subq(elem))"
            ).format(subquery=subquery)
        else:
            json_agg = sql.SQL(
                "COALESCE((SELECT jsonb_agg(subq.elem) FROM ({subquery}) AS subq(elem)), '[]')"
            ).format(subquery=subquery)

        # --- Step 5: Register JOIN and SELECT field ---
        self.join(join_type, table, on, alias)
        self._select.append((json_agg, json_field_name))

        # --- Step 6: Ensure GROUP BY parent ID ---
        if self._table_alias:
            self._group_by_fields.append(f"{self._table_alias}.id")
        else:
            self._group_by_fields.append("id")

        return self


    @staticmethod
    def build_filter_sql(conditions: Dict[str, Any]) -> sql.Composed:
        clauses = []

        for key, value in conditions.items():
            if "__" in key:
                col, op = key.split("__", 1)
            else:
                col, op = key, "eq"

            table_name, col_name = col.split(".")
            col_ref = sql.SQL("{}.{}").format(
                sql.Identifier(table_name), sql.Identifier(col_name)
            )

            if op == "eq":
                clauses.append(sql.SQL("{} = {}").format(col_ref, sql.Literal(value)))
            elif op == "ne":
                clauses.append(sql.SQL("{} != {}").format(col_ref, sql.Literal(value)))
            elif op == "gt":
                clauses.append(sql.SQL("{} > {}").format(col_ref, sql.Literal(value)))
            elif op == "lt":
                clauses.append(sql.SQL("{} < {}").format(col_ref, sql.Literal(value)))
            elif op == "gte":
                clauses.append(sql.SQL("{} >= {}").format(col_ref, sql.Literal(value)))
            elif op == "lte":
                clauses.append(sql.SQL("{} <= {}").format(col_ref, sql.Literal(value)))
            elif op == "in":
                values_sql = sql.SQL(", ").join(sql.Literal(v) for v in value)
                clauses.append(sql.SQL("{} IN ({})").format(col_ref, values_sql))
            elif op == "notin":
                values_sql = sql.SQL(", ").join(sql.Literal(v) for v in value)
                clauses.append(sql.SQL("{} NOT IN ({})").format(col_ref, values_sql))
            elif op == "isnull":
                if value:
                    clauses.append(sql.SQL("{} IS NULL").format(col_ref))
                else:
                    clauses.append(sql.SQL("{} IS NOT NULL").format(col_ref))
            elif op == "notnull":
                clauses.append(sql.SQL("{} IS NOT NULL").format(col_ref))
            else:
                raise ValueError(f"Unsupported operator: {op}")

        return sql.SQL(" AND ").join(clauses)


    async def fetch_one(self):
        query, param = self.build()
        try:
            row = await self.connection.fetchrow(query.as_string(), *param)
            return row
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error occurred while fetching one: {e}")


    def debug_sql(self):
        query, params = self.build()
        return query.as_string(), params


    @staticmethod
    def get_field_name(model: Type[BaseModel], field_name: str) -> Optional[str]:
        """
        Returns the field name if it exists in the model, else None.

        Example:
            get_model_field_name(AnnualPlan, "name")  ➜ "name"
            get_model_field_name(AnnualPlan, "fake")  ➜ None
        """
        return field_name if field_name in model.model_fields else None
