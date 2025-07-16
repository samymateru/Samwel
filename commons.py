from psycopg import AsyncConnection, sql
from fastapi import HTTPException

async def get_module_user(connection: AsyncConnection, module_id: str, user_id: str):
    query = sql.SQL("""
        SELECT
          u_data ->> 'id' AS id,
          u_data ->> 'type' AS type,
          u_data ->> 'role' AS role,
          u_data ->> 'title' AS title,
          u_data -> 'engagements' AS engagements,
          u.name,
          u.email,
          u.telephone
        FROM modules m
        JOIN LATERAL jsonb_array_elements(m.users) AS u_data ON true
        JOIN users u ON u.id = u_data ->> 'id'
        WHERE m.id = {module_id}
        {user_filter}
    """).format(
        module_id=sql.Placeholder("module_id"),
        user_filter=sql.SQL("AND u_data ->> 'id' = {user_id}").format(
            user_id=sql.Placeholder("user_id")
        ) if user_id else sql.SQL("")
    )

    params = {"module_id": str(module_id)}
    if user_id:
        params["user_id"] = str(user_id)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users by email {e}")

async def get_role(connection: AsyncConnection, name: str, module_id: str):
    query = sql.SQL("SELECT * FROM public.roles WHERE name = %s AND module = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (name, module_id))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying roles {e}")