from AuditNew.Internal.engagements.planning.schemas import *
from utils import get_next_reference
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.control.databases import *
from psycopg import AsyncConnection, sql
import json
from psycopg.errors import ForeignKeyViolation, UniqueViolation


def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'



async def add_summary_audit_program(connection: AsyncConnection, procedure_id: str, prcm_id: str, reference: str):
    query = sql.SQL(
        """
        UPDATE public."PRCM" 
        SET 
        summary_audit_program = %s,
        reference = %s
        WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (procedure_id, reference, prcm_id))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding summary of audit program {e}")



async def add_planning_procedure(connection: AsyncConnection, procedure: NewPlanningProcedure, engagement_id: str):
    data = {
            "title": f"{procedure.title}",
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
            "objectives": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": None,
            "reviewed_by": None
        }
    query = sql.SQL(
        """
           INSERT INTO public.std_template (
                id,
                engagement,
                reference,
                title,
                tests,
                results,
                observation,
                attachments,
                conclusion,
                objectives,
                type,
                prepared_by,
                reviewed_by,
                status
           ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            ref = await get_next_reference(connection=connection, resource="std_template", engagement_id=engagement_id)
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
                json.dumps(data["objectives"]),
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
        raise HTTPException(status_code=409, detail="Planning procedure already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding planning procedures {e}")



async def get_planning_procedures(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.std_template WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching planning procedures {e}")



async def edit_planning_procedure(connection: AsyncConnection, std_template: StandardTemplate, procedure_id: str):
    query = sql.SQL(
        """
            UPDATE public.std_template
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
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                std_template.title,
                safe_json_dump(std_template.tests),
                safe_json_dump(std_template.results),
                safe_json_dump(std_template.observation),
                std_template.attachments,
                safe_json_dump(std_template.conclusion),
                safe_json_dump(std_template.prepared_by),
                safe_json_dump(std_template.reviewed_by),
                procedure_id
            ))
            await connection.commit()

    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Invalid procedure id passe")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating planning procedure {e}")


####################################################################################################################


async def save_procedure_(connection: AsyncConnection, procedure: SaveProcedure, procedure_id: str, resource: str):
    procedure_types = {
        "Planning": "std_template",
        "Reporting": "reporting_procedure",
        "Finalization": "finalization_procedure"
    }
    query = sql.SQL(
        """
            UPDATE {resource}
            SET 
            tests = %s::jsonb,
            objectives = %s::jsonb,
            results = %s::jsonb,
            observation = %s::jsonb,
            conclusion = %s::jsonb
            WHERE id = %s; 
        """).format(resource=sql.Identifier('public', procedure_types.get(resource)))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                safe_json_dump(procedure.tests),
                safe_json_dump(procedure.objectives),
                safe_json_dump(procedure.results),
                safe_json_dump(procedure.observation),
                safe_json_dump(procedure.conclusion),
                procedure_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving procedure {e}")



async def prepare_std_template(connection: AsyncConnection, procedure: PreparedReviewedBy, procedure_id: str, resource: str):
    procedure_types = {
        "Planning": "std_template",
        "Reporting": "reporting_procedure",
        "Finalization": "finalization_procedure"
    }
    query = sql.SQL(
        """
        UPDATE {resource}
        SET 
        prepared_by = %s::jsonb
        WHERE id = %s; 
        """).format(resource=sql.Identifier('public', procedure_types.get(resource)))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                procedure.model_dump_json(),
                procedure_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error preparing {resource} procedure {e}")



async def review_std_template(
        connection: AsyncConnection,
        procedure: PreparedReviewedBy,
        procedure_id: str,
        resource: str
):
    procedure_types = {
        "Planning": "std_template",
        "Reporting": "reporting_procedure",
        "Finalization": "finalization_procedure"
    }
    query = sql.SQL(
        """
        UPDATE {resource}
        SET 
        reviewed_by = %s::jsonb
        WHERE id = %s; 
        """).format(resource=sql.Identifier('public', procedure_types.get(resource)))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                procedure.model_dump_json(),
                procedure_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error preparing {resource} procedure {e}")
