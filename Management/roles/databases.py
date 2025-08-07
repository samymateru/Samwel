import json
from typing import Union

from fastapi import HTTPException
from Management.roles.schemas import *
from psycopg import AsyncConnection, sql
from utils import get_unique_key, get_latest_reference_number


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
        engagements,
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
        %s, %s, %s, %s, %s, %s, %s,
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
            if reference == 0:
                reference = reference + 10
            else:
                reference = reference + 1
            await cursor.execute(query, (
                module_id,
                get_unique_key(),
                role.name,
                f"ROLE-{reference:03}",
                role.section,
                role.type,
                role.settings,
                role.audit_plans,
                role.engagements,
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

async def edit_role(connection: AsyncConnection, role: EditRole, role_id: str, module_id: str):
    query = sql.SQL(
        """
        UPDATE public.roles
        SET 
        name = %s,
        section = %s,
        type = %s,
        settings = %s,
        audit_plans = %s,
        engagements = %s,
        administration = %s,
        planning = %s,
        fieldwork = %s,
        reporting = %s,
        audit_program = %s,
        follow_up = %s,
        issue_management = %s,
        archive_audit = %s,
        un_archive_audit = %s,
        others = %s
        WHERE id = %s AND module = %s;
    """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                role.name,
                role.section,
                role.type,
                role.settings,
                role.audit_plans,
                role.engagements,
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
                role_id,
                module_id
            ))

        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating roles {e}")




