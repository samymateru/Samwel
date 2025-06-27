from fastapi import HTTPException

from psycopg import AsyncConnection, sql

from AuditNew.Internal.engagements.attachments.schemas import *

async def add_procedure_attachment(connection: AsyncConnection, attachment: Attachment):
    query = sql.SQL(
        """
        INSERT INTO public.attachments 
        (
        id,
        engagement,
        procedure,
        url,
        name,
        size,
        type,
        section,
        creator_name,
        creator_email,
        created_at
        )
        VALUES 
        (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                attachment.id,
                attachment.engagement,
                attachment.procedure,
                attachment.url,
                attachment.name,
                attachment.size,
                attachment.type,
                attachment.section,
                attachment.creator_name,
                attachment.creator_email,
                attachment.created_at
            ))
            await connection.commit()
    except HTTPException:
        raise

async def get_procedure_attachment(connection: AsyncConnection, engagement_id: str, procedure_id: str):
    query = sql.SQL(
    """
    SELECT * FROM public.attachments WHERE engagement = %s AND procedure = %s
    """).format()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id, procedure_id))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching attachment {e}")

