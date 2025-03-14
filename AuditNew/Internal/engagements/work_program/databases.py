from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.work_program.schemas import *
from utils import get_reference


def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

def add_new_main_program(connection: Connection, program: MainProgram, engagement_id: int):
    query: str = """
                     INSERT INTO public.main_program (engagement, name) VALUES (%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                engagement_id,
                program.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating main program {e}")

def add_new_sub_program(connection: Connection, sub_program: NewSubProgram, program_id: int):
    query: str = """
                     INSERT INTO public.sub_program (
                                program,
                                reference,
                                title,
                                brief_description,
                                audit_objective,
                                test_description,
                                test_type,
                                sampling_approach,
                                results_of_test,
                                observation,
                                extended_testing,
                                extended_procedure,
                                extended_results,
                                effectiveness,
                                conclusion
                                ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        reference = get_reference(connection=connection, resource="sub_program", id=program_id)
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                program_id,
                reference,
                sub_program.title,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                True,
                "",
                "",
                "",
                ""
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating sub program {e}")

def add_new_sub_program_evidence(connection: Connection, evidence: SubProgramEvidence, sub_program_id: int):
    query: str = """
                       INSERT INTO public.sub_program_evidence (
                           sub_program,
                           attachment
                           ) VALUES (%s, %s); 
                    """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                sub_program_id,
                evidence.attachment
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating sub program evidence {e}")

def get_sub_program_evidence(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public.sub_program_evidence
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
        raise HTTPException(status_code=400, detail=f"Error fetching sub program evidence {e}")

def get_main_program(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public.main_program
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
        raise HTTPException(status_code=400, detail=f"Error fetching main program {e}")

def get_sub_program(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                   SELECT * from public.sub_program
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
        raise HTTPException(status_code=400, detail=f"Error fetching sub program {e}")

def remove_work_program(connection: Connection, id: int, table: str, resource: str):
    query: str = f"DELETE FROM public.{table} WHERE id = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting {resource} {e}")

def edit_sub_program(connection: Connection, sub_program: SubProgram, program_id: int):
    query: str = """
                    UPDATE public.sub_program
                    SET 
                    title = %s,
                    brief_description = %s,
                    audit_objective = %s,
                    test_description = %s,
                    test_type = %s,
                    sampling_approach = %s,
                    results_of_test = %s,
                    observation = %s,
                    extended_testing = %s,
                    extended_procedure = %s,
                    extended_results = %s,
                    effectiveness = %s,
                    conclusion = %s WHERE id = %s; 
                   """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                sub_program.title,
                sub_program.brief_description,
                sub_program.audit_objective,
                sub_program.test_description,
                sub_program.test_type,
                sub_program.sampling_approach,
                sub_program.results_of_test,
                sub_program.observation,
                sub_program.extended_testing,
                sub_program.extended_procedure,
                sub_program.extended_results,
                sub_program.effectiveness,
                sub_program.conclusion,
                program_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating sub program procedure {e}")

def edit_main_program(connection: Connection, program: MainProgram, program_id: int):
    query = """
        UPDATE public.task
        SET 
        name = %s
        WHERE id = %s;
        """
    values = (
        program.name,
        program
    )
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating main program {e}")




