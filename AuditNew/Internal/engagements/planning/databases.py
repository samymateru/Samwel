import json
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from AuditNew.Internal.engagements.planning.schemas import *
from psycopg2.extensions import cursor as Cursor
from utils import get_next_reference

def add_engagement_letter(connection: Connection, letter: EngagementLetter, engagement_id: int):
    query: str = """
                   INSERT INTO public.engagement_letter (
                        engagement,
                        name,
                        date_attached,
                        attachment
                   ) VALUES(%s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                letter.name,
                letter.date_attached,
                letter.attachment
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement letter {e}")

def add_engagement_prcm(connection: Connection, prcm: PRCM, engagement_id: int):
    query: str = """
                   INSERT INTO public."PRCM" (
                        engagement,
                        process,
                        risk,
                        risk_rating,
                        control,
                        control_objective,
                        control_type,
                        residue_risk
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                prcm.process.model_dump_json(),
                prcm.risk.model_dump_json(),
                prcm.risk_rating,
                prcm.control.model_dump_json(),
                prcm.control_objective.model_dump_json(),
                prcm.control_type,
                prcm.residue_risk
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement PRCM {e}")


def add_summary_audit_program(connection: Connection, summary: SummaryAuditProgram, engagement_id: int):
    query: str = """
                   INSERT INTO public.summary_audit_program (
                        engagement,
                        process,
                        risk,
                        risk_rating,
                        control,
                        procedure,
                        program
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                summary.process.model_dump_json(),
                summary.risk.model_dump_json(),
                summary.risk_rating,
                summary.control.model_dump_json(),
                summary.procedure,
                summary.program,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding summary of audit program {e}")

def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

def add_planning_procedure(connection: Connection, procedure: NewPlanningProcedure, engagement_id: int):
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
    query: str = """
                   INSERT INTO public.std_template (
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
                        reviewed_by
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            ref = get_next_reference(connection=connection, resource="std_template", engagement=engagement_id)
            cursor.execute(query, (
                engagement_id,
                ref,
                data["title"],
                json.dumps(data["tests"]),
                json.dumps(data["results"]),
                json.dumps(data["observation"]),
                data["attachments"],
                json.dumps(data["conclusion"]),
                data["type"],
                json.dumps(data["prepared_by"]),
                json.dumps(data["reviewed_by"])
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding planning procedures {e}")

def get_planning_procedures(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public.std_template
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching planning procedures {e}")

def get_prcm(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public."PRCM"
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement PRCM {e}")

def get_engagement_letter(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public.engagement_letter
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement letter {e}")

def get_summary_audit_program(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public.summary_audit_program
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of audit program {e}")

def edit_planning_procedure(connection: Connection, std_template: StandardTemplate, procedure_id: int):
    query: str = """
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
                   """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
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
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating planning procedure {e}")

