import json
from fastapi import HTTPException
from Management.roles.schemas import *
from psycopg import AsyncConnection, sql

from utils import get_latest_reference_number


async def get_roles(connection: AsyncConnection, module_id: str):
    query = sql.SQL("SELECT * FROM public.roles WHERE module = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying roles {e}")

async def add_role(connection: AsyncConnection, role: Roles, module_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.roles (
        module,
        id,
        name,
        reference,
        section,
        type,
        settings,
        audit_plans,
        administration,
        planning,
        fieldwork,
        reporting,
        audit_program,
        follow_up,
        issue_management,
        archive_audit,
        un_archive_audit,
        others,
        created_at
    ) VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s
    );
    """)

    query_role_reference = sql.SQL(
        """
        SELECT reference from public.roles WHERE module = {module}
        """).format(module=sql.Literal(module_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query_role_reference)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            references_data =[dict(zip(column_names, row_)) for row_ in rows]
            reference = int(get_latest_reference_number(references_data=references_data))
            print(reference)
            if reference == 0:
                reference = reference + 8
            else:
                reference = reference + 1
            await cursor.execute(query, (
                module_id,
                role.id,
                role.name,
                f"ROLE-{reference:03}",
                role.section,
                role.type,
                role.settings,
                role.audit_plans,
                role.administration,
                role.planning,
                role.fieldwork,
                role.reporting,
                role.audit_program,
                role.follow_up,
                role.issue_management,
                role.archive_audit,
                role.un_archive_audit,
                role.others,
                role.created_at
            ))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating role {e}")

async def edit_role(connection: AsyncConnection, role: Category, company_id: str, name: str):
    query = sql.SQL("""
                   UPDATE roles
                   SET roles = %s::jsonb
                   WHERE company = %s;
                 """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT roles FROM roles WHERE company = %s;", (company_id,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=203, detail="No roles")
            roles = result[0]
            for role_ in roles:
                if role_["name"] == name:
                    role_["name"] = role.name  # Update the role name
                    role_["permissions"] = role.permissions.model_dump()  # Update permissions
                    break
            await cursor.execute(query, (json.dumps(roles), company_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating roles {e}")



