from fastapi import HTTPException
from AuditNew.Internal.engagements.finalizations.schemas import *
from AuditNew.Internal.engagements.planning.schemas import StandardTemplate
from utils import get_next_reference
import json
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from utils import get_unique_key

def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'


async def add_finalization_procedure(connection: AsyncConnection, finalization: NewFinalizationProcedure, engagement_id: str):
    data = {
        "title": finalization.title,
        "tests": {
            "value": ""
        },
        "results": {
            "value": ""
        },
        "observation": {
            "value": ""
        },
        "attachments": [
            ""
        ],
        "conclusion": {
            "value": ""
        },
        "type": "standard",
        "prepared_by": {
            "id": 0,
            "name": ""
        },
        "reviewed_by": {
            "id": 0,
            "name": ""
        }
    }
    query = sql.SQL(
        """
        INSERT INTO public.finalization_procedure (
            id,
            engagement,
            reference,
            title,
            tests,
            results,
            observation,
            attachments,
            conclusion,
            type,
            prepared_by,
            reviewed_by,
            status
        ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            ref = await get_next_reference(connection=connection, resource="finalization_procedure", engagement_id=engagement_id)
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                ref,
                data["title"],
                json.dumps(data["tests"]),
                json.dumps(data["results"]),
                json.dumps(data["observation"]),
                data["attachments"],
                json.dumps(data["conclusion"]),
                data["type"],
                None,
                None,
                "Pending"
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Finalization procedure already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding finalization procedures {e}")

async def get_finalization_procedures(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.finalization_procedure WHERE engagement = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching finalization procedures {e}")

async def edit_finalization_procedure(connection: AsyncConnection, finalization: StandardTemplate, procedure_id: str):
    query = sql.SQL(
        """
        UPDATE public.finalization_procedure
        SET 
        title = %s,
        tests = %s::jsonb,
        results = %s::jsonb,
        observation = %s::jsonb,
        attachments = %s,
        conclusion = %s::jsonb,
        prepared_by = %s::jsonb,
        reviewed_by = %s::jsonb  WHERE id = %s; 
        """)
    update_procedure_status = sql.SQL(
        """
        UPDATE public.finalization_procedure
        SET 
        status = %s
        WHERE id = %s; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                finalization.title,
                safe_json_dump(finalization.tests),
                safe_json_dump(finalization.results),
                safe_json_dump(finalization.observation),
                finalization.attachments,
                safe_json_dump(finalization.conclusion),
                safe_json_dump(finalization.prepared_by),
                safe_json_dump(finalization.reviewed_by),
                procedure_id
            ))
            await connection.commit()
            if finalization.reviewed_by.id == "0" or finalization.reviewed_by.name == "":
                await cursor.execute(update_procedure_status, ("In progress", procedure_id))
            else:
                await cursor.execute(update_procedure_status, ("Completed", procedure_id))
            await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Finalization procedure already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating finalization procedure {e}")