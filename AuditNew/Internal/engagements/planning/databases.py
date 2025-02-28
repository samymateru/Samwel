from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from AuditNew.Internal.engagements.planning.schemas import *
from psycopg2.extensions import cursor as Cursor

def add_engagement_letter(connection: Connection, letter: EngagementLetter, engagement_id: int):
    query: str = """
                   INSERT INTO public.engagement_letter (
                        engagement,
                        name,
                        value
                   ) VALUES(%s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                letter.name,
                letter.value
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement letter {e}")

def add_engagement_prcm(connection: Connection, prcm: PRCM, engagement_id: int):
    query: str = """
                   INSERT INTO public.PRCM (
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
                prcm.process,
                prcm.risk,
                prcm.risk_rating,
                prcm.control,
                prcm.control_objective,
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
                summary.process,
                summary.risk,
                summary.risk_rating,
                summary.control,
                summary.procedure,
                summary.program,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding summary of audit program {e}")

def get_prcm(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public.PRCM
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