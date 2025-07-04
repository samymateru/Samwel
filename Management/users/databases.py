from fastapi import HTTPException
from utils import generate_hash_password
from Management.users.schemas import *
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from utils import get_unique_key

async def new_user(connection: AsyncConnection, user: User, organization_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.users (id, organization, name, email, telephone, password_hash, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)

    check_user_query = sql.SQL(
        """
        SELECT id, organization FROM public.users WHERE email = %s 
        """)

    update_user_query = sql.SQL(
        """
        UPDATE public.users
        SET organization = organization || %s
        WHERE id = %s RETURNING id;
        """)

    update_module_query = sql.SQL(
        """
        UPDATE public.modules 
        SET users = COALESCE(users, '[]'::jsonb) || %s::jsonb
        WHERE id = %s;
        """)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(check_user_query, (user.email, ))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows]
            if user_data.__len__() == 0:
                await cursor.execute(query, (
                    get_unique_key(),
                    [organization_id],
                    user.name,
                    user.email,
                    user.telephone,
                    generate_hash_password(user.password),
                    datetime.now()
                ))
                user_id = await cursor.fetchone()
                user_type = UserType(
                    id = user_id[0],
                    type = user.type,
                    role = user.role,
                    title = user.title,
                    engagements=[]
                )
                await cursor.execute(update_module_query, (f"[{user_type.model_dump_json()}]", user.module))
                await connection.commit()
                return user_id[0]

            else:
                if organization_id not in user_data[0].get("organization"):
                    await cursor.execute(update_user_query, ([organization_id], user_data[0].get("id")))
                    user_id = await cursor.fetchone()
                    user_type = UserType(
                        id=user_id[0],
                        type=user.type,
                        role=user.role,
                        title=user.title,
                        engagements=[]
                    )
                    await cursor.execute(update_module_query, (f"[{user_type.model_dump_json()}]", user.module))
                    await connection.commit()
                    return user_id[0]
                else:
                    raise HTTPException(status_code=400, detail="Users exists in this organization")
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid organization id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="User already exist")
    except HTTPException as e:
        await connection.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating new user {e}")

async def new_owner(connection: AsyncConnection, user: User, organization_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.users (id, organization, name, email, telephone, password_hash, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)

    check_user_query = sql.SQL(
        """
        SELECT id, organization FROM public.users WHERE email = %s 
        """)

    update_user_query = sql.SQL(
        """
        UPDATE public.users 
        SET organization = organization || %s
        WHERE id = %s RETURNING id;
        """)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(check_user_query, (user.email, ))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows]
            if user_data.__len__() == 0:
                await cursor.execute(query, (
                    get_unique_key(),
                    [organization_id],
                    user.name,
                    user.email,
                    user.telephone,
                    generate_hash_password(user.password),
                    datetime.now()
                ))
                user_id = await cursor.fetchone()
                await connection.commit()
                return user_id[0]
            else:
                if organization_id not in user_data[0].get("organization"):
                    await cursor.execute(update_user_query, ([organization_id], user_data[0].get("id")))
                    user_id = await cursor.fetchone()
                    await connection.commit()
                    return user_id[0]
                else:
                    raise HTTPException(status_code=400, detail="Users exists in this organization")
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid organization id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="User already exist")
    except HTTPException as e:
        await connection.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating new user {e}")


async def delete_user(connection: AsyncConnection, user_id: str):
    query = sql.SQL("DELETE FROM public.users WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting the user {e}")

async def get_user(connection: AsyncConnection, user_id: str):
    query = sql.SQL("SELECT * FROM public.users WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying user {e}")

async def get_users(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * FROM public.users WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users {e}")

async def get_organizations_users(connection: AsyncConnection, organization_id: str):
    query = sql.SQL(
        """
        SELECT * FROM public.users WHERE id = ANY(%s);
        """)

    user_list_query = sql.SQL(
        """
        SELECT users FROM public.organization WHERE id = {organization_id};
        """).format(organization_id=sql.Literal(organization_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(user_list_query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_ids = [dict(zip(column_names, row_)) for row_ in rows]
            await cursor.execute(query, (user_ids[0].get("users"),))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows]
            return user_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users by email {e}")

async def get_module_users(connection: AsyncConnection, module_id: str):
    query = sql.SQL(
        """
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
        WHERE m.id = {module_id};
        """).format(module_id=sql.Literal(module_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows]
            return user_data
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users by email {e}")

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


async def get_user_by_email(connection: AsyncConnection, email: str):
    query = sql.SQL("SELECT * FROM public.users WHERE email = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (email,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users by email {e}")

async def edit_user(connection: AsyncConnection, user: User, user_id: str):
    query = sql.SQL(
        """
        UPDATE modules
        SET users = (
            SELECT jsonb_agg(
                CASE
                    WHEN item->>'id' = %s THEN
                        jsonb_set(
                            jsonb_set(item, '{role}', to_jsonb(%s::text)),
                            '{title}', to_jsonb(%s::text)
                        )
                    ELSE item
                END
            )
            FROM jsonb_array_elements(users) AS item
        )
        WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id, user.role, user.title, user.module))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying company modules {e}")