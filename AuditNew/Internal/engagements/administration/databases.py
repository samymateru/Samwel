import json
from fastapi import HTTPException
from AuditNew.Internal.engagements.administration.schemas import *
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from AuditNew.Internal.engagements.administration.schemas import __Staff__
from utils import get_unique_key



async def add_new_business_contact(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.business_contact (
            id,
            engagement,
            "user",
            type
        ) 
        VALUES(%s, %s, %s::jsonb, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                json.dumps([]),
                "Action"
            ))
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                json.dumps([]),
                "Information"
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding business contact {e}")


async def get_business_contacts(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.business_contact WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching business contacts {e}")


async def edit_business_contact(connection: AsyncConnection, business_contact: BusinessContact, engagement_id: str):
    query = sql.SQL(
        """
          UPDATE public.business_contact
          SET 
          "user" = %s::jsonb
          WHERE engagement = %s AND type = %s
        """)
    try:
        async with connection.cursor() as cursor:

            await cursor.execute(query, (
                json.dumps(business_contact.model_dump().get("user")),
                engagement_id,
                business_contact.type
                ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating business contact {e}")

