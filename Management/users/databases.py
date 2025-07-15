from fastapi import HTTPException
from utils import check_row_exists, get_unique_key, generate_hash_password
from Management.users.schemas import *
from psycopg import AsyncConnection, sql

async def create_new_user(connection: AsyncConnection, new_user: User):
    query = sql.SQL(
        """
        INSERT INTO public.users
        (
         id,
         entity,
         name,
         email,
         telephone,
         password_hash,
         administrator,
         owner,
         created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="users", filters={
                "email": new_user.email
            })
            if exists:
                raise HTTPException(status_code=400, detail="User exists")
            await cursor.execute(query=query, params=(
                new_user.id,
                new_user.entity_id,
                new_user.name,
                new_user.email,
                new_user.telephone,
                new_user.password,
                new_user.administrator,
                new_user.owner,
                new_user.created_at
            ))
            user_id = await cursor.fetchone()
            await connection.commit()
            return user_id[0]
    except HTTPException:
        await connection.rollback()
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating new user {e}")

async def attach_user_to_organization(connection: AsyncConnection, attach_data: OrganizationsUsers):
    query = sql.SQL(
        """
        INSERT INTO public.organizations_users
        (
         organization_id,
         user_id,
         administrator,
         owner,
         created_at
        ) VALUES (%s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="organizations_users", filters={
                "organization_id": attach_data.organization_id,
                "user_id": attach_data.user_id
            })
            if exists:
                return
            await cursor.execute(query=query, params=(
                attach_data.organization_id,
                attach_data.user_id,
                attach_data.administrator,
                attach_data.owner,
                attach_data.created_at
            ))
            await connection.commit()
    except HTTPException:
        await connection.rollback()
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error attaching user to the organization {e}")

async def attach_user_to_module(connection: AsyncConnection, attach_data: ModulesUsers):
    query = sql.SQL(
        """
        INSERT INTO public.modules_users
        (
         module_id,
         user_id,
         title,
         role,
         type,
         created_at
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="modules_users", filters={
                "module_id": attach_data.module_id,
                "user_id": attach_data.user_id
            })
            if exists:
                return
            await cursor.execute(query=query, params=(
                attach_data.module_id,
                attach_data.user_id,
                attach_data.title,
                attach_data.role,
                attach_data.type,
                attach_data.created_at
            ))
            await connection.commit()
    except HTTPException:
        await connection.rollback()
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error attaching user to the module {e}")

async def invite_user(connection: AsyncConnection, entity_id: str, organization_id: str, new_user: NewUser):
    check_user = sql.SQL(
        """
        SELECT id FROM public.users WHERE email = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(check_user, (new_user.email,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            if data.__len__() != 0:
                attach_data = OrganizationsUsers(
                    organization_id=organization_id,
                    user_id=data[0].get("id"),
                    administrator=False,
                    owner=False
                )

                await attach_user_to_organization(connection=connection, attach_data=attach_data)

                attach_data = ModulesUsers(
                    module_id=new_user.module_id,
                    user_id=data[0].get("id"),
                    title=new_user.title,
                    role=new_user.role,
                    type=new_user.type
                )

                await attach_user_to_module(connection=connection, attach_data=attach_data)
            else:
                _new_user_ = User(
                    id=get_unique_key(),
                    name=new_user.name,
                    email=new_user.email,
                    telephone=new_user.telephone,
                    password=generate_hash_password("123456"),
                    administrator=False,
                    owner=False,
                    entity_id=entity_id
                )

                user_id = await create_new_user(connection=connection, new_user=_new_user_)

                attach_data = OrganizationsUsers(
                    organization_id=organization_id,
                    user_id=user_id,
                    administrator=False,
                    owner=False
                )

                await attach_user_to_organization(connection=connection, attach_data=attach_data)
                attach_data = ModulesUsers(
                    module_id=new_user.module_id,
                    user_id=user_id,
                    title=new_user.title,
                    role=new_user.role,
                    type=new_user.type
                )



                await attach_user_to_module(connection=connection, attach_data=attach_data)
    except HTTPException:
        await connection.rollback()
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error invite user to the module {e}")

async def get_entity_users(connection: AsyncConnection, entity_id: str):
    query = sql.SQL(
        """
        SELECT * FROM public.users WHERE entity = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (entity_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying entity users {e}")

async def get_organizations_users(connection: AsyncConnection, organization_id: str):
    query = sql.SQL(
        """
        SELECT 
          usr.id,
          usr.entity,
          org_usr.organization_id as organization,
          usr.name,
          usr.email,
          usr.telephone,
          usr.created_at,
          org_usr.administrator,
          org_usr.owner,
          COALESCE(
            JSON_AGG(
              JSON_BUILD_OBJECT(
                'id',    mod_usr.module_id,
                'title', mod_usr.title,
                'role',  mod_usr.role,
                'type',  mod_usr.type,
                'name',  mod.name
              )
            ) FILTER (WHERE mod_usr.module_id IS NOT NULL),
            '[]'::json
          ) AS modules
        FROM public.organizations_users org_usr
        JOIN public.users usr ON usr.id = org_usr.user_id
        LEFT JOIN public.modules_users mod_usr ON mod_usr.user_id = org_usr.user_id
        LEFT JOIN public.modules mod ON mod.id = mod_usr.module_id
          AND mod.organization = org_usr.organization_id
        WHERE org_usr.organization_id = %s
        GROUP BY 
          usr.id,
          usr.entity,
          org_usr.organization_id,
          usr.name,
          usr.email,
          usr.telephone,
          usr.created_at,
          org_usr.administrator,
          org_usr.owner;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(organization_id,))
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
        usr.id,
        usr.entity,
        mod_usr.module_id as module,
        usr.name,
        usr.email,
        usr.telephone,
        usr.created_at,
        mod_usr.title,
        mod_usr.role,
        mod_usr.type 
        FROM public.modules_users mod_usr
        JOIN public.users usr ON usr.id = mod_usr.user_id
        WHERE  mod_usr.module_id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows]
            return user_data
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching module users {e}")

async def get_module_user(connection: AsyncConnection, module_id: str, user_id: str):
    query = sql.SQL(
        """
        SELECT 
        usr.id,
        usr.entity,
        mod_usr.module_id as module,
        usr.name,
        usr.email,
        usr.telephone,
        usr.created_at,
        mod_usr.title,
        mod_usr.role 
        FROM public.modules_users mod_usr
        JOIN public.users usr ON usr.id = mod_usr.user_id
        WHERE  mod_usr.module_id = %s AND usr.id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (module_id, user_id))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching module user {e}")

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

async def remove_module(connection: AsyncConnection, module_id: str):
    delete_modules_users = sql.SQL("DELETE FROM public.modules_users WHERE module_id = %s;")
    delete_module = sql.SQL("DELETE FROM public.modules WHERE id = %s;")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(delete_modules_users,(module_id,))
            await cursor.execute(delete_module,(module_id,))
        await connection.commit()
    except HTTPException:
        await connection.rollback()
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting module {e}")