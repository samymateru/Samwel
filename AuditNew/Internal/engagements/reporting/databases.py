from fastapi import HTTPException
from AuditNew.Internal.engagements.reporting.schemas import *
from AuditNew.Internal.engagements.planning.schemas import StandardTemplate
import json
from utils import get_next_reference, get_unique_key
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation


def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

async def add_reporting_procedure(connection: AsyncConnection, report: NewReportingProcedure, engagement_id: str):
    data = {
        "title": report.title,
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
           INSERT INTO public.reporting_procedure (
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
            ref = await get_next_reference(connection=connection, resource="reporting_procedure", engagement_id=engagement_id)
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
        raise HTTPException(status_code=409, detail="Report procedure already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding reporting procedures {e}")

async def get_reporting_procedures(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.reporting_procedure WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching reporting procedures {e}")

async def edit_reporting_procedure(connection: AsyncConnection, report: StandardTemplate, procedure_id: str):
    query = sql.SQL(
        """
            UPDATE public.reporting_procedure
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
        UPDATE public.reporting_procedure
        SET 
        status = %s
        WHERE id = %s; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                report.title,
                safe_json_dump(report.tests),
                safe_json_dump(report.results),
                safe_json_dump(report.observation),
                report.attachments,
                safe_json_dump(report.conclusion),
                safe_json_dump(report.prepared_by),
                safe_json_dump(report.reviewed_by),
                procedure_id
            ))
            await connection.commit()
            if report.reviewed_by.id == "0" or report.reviewed_by.name == "":
                await cursor.execute(update_procedure_status, ("In progress", procedure_id))
            else:
                await cursor.execute(update_procedure_status, ("Completed", procedure_id))
            await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Report procedure already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating reporting procedure {e}")

async def get_summary_findings(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * FROM public.issue WHERE engagement = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue based on engagement {e}")

async def get_summary_audit_process(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
            SELECT 
            main_program.id,
            main_program.name,
            main_program.status,
            main_program.process_rating,
            COUNT(issue.id) AS issue_count,
            COUNT(CASE WHEN issue.risk_rating = 'Acceptable' THEN 1 END) AS acceptable,
            COUNT(CASE WHEN issue.risk_rating = 'Improvement Required' THEN 1 END) AS improvement_required,
            COUNT(CASE WHEN issue.risk_rating = 'Significant Improvement Required' THEN 1 END) AS significant_improvement_required,
            COUNT(CASE WHEN issue.risk_rating = 'Unacceptable' THEN 1 END) AS Unacceptable,
            COUNT(CASE WHEN issue.recurring_status = true THEN 1 END) AS recurring_issues
            FROM engagements 
            JOIN main_program ON main_program.engagement = engagements.id
            LEFT JOIN sub_program ON sub_program.program = main_program.id
            LEFT JOIN issue ON sub_program.id = issue.sub_program
            WHERE main_program.engagement = %s
            GROUP BY main_program.name, main_program.status, main_program.process_rating, main_program.id; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of audit process {e}")

