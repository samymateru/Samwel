from typing import Dict, List
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.work_program.schemas import *
from utils import get_next_reference


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

def add_new_sub_program(connection: Connection, sub_program: SubProgram, program_id: int):
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
                                conclusion,
                                reviewed_by,
                                prepared_by
                                ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        reference = get_next_reference(connection, )
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                program_id,
                sub_program.reference,
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
                sub_program.reviewed_by,
                sub_program.prepared_by
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating sub program {e}")

def add_new_issue(connection: Connection, issue: Issue, sub_program_id: int):
    query: str = """
                    INSERT INTO public.your_table_name (
                            sub_program,
                            title,
                            criteria,
                            finding,
                            risk_rating,
                            process,
                            sub_process,
                            root_cause_description,
                            root_cause,
                            sub_root_cause,
                            risk_category,
                            sub_risk_category,
                            impact_description,
                            impact_category,
                            impact_sub_category,
                            recurring_status,
                            recommendation,
                            management_action_plan,
                            estimated_implementation_date,
                            implementation_contacts
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                sub_program_id,
                issue.title,
                issue.criteria,
                issue.finding,
                issue.risk_rating,
                issue.process,
                issue.sub_process,
                issue.root_cause_description,
                issue.root_cause,
                issue.sub_root_cause,
                issue.risk_category,
                issue.sub_risk_category,
                issue.impact_description,
                issue.impact_category,
                issue.impact_sub_category,
                issue.recurring_status,
                issue.recommendation,
                issue.management_action_plan,
                issue.estimated_implementation_date,
                issue.implementation_contacts
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating issue {e}")

def add_new_task(connection: Connection, task: Task, sub_program_id: int):
    query: str = """
                    INSERT INTO public.task (
                        sub_program,
                        title,
                        reference,
                        description,
                        date_raised,
                        raised_by,
                        action_owner,
                        resolution_summary,
                        resolution_details,
                        resolved_by,
                        date_resolved,
                        decision
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                sub_program_id,
                task.title,
                task.reference,
                task.description,
                task.date_raised,
                task.raised_by,
                task.action_owner,
                task.resolution_summary,
                task.resolution_details,
                task.resolved_by,
                task.date_resolved,
                task.decision
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating task {e}")

def add_new_review_note(connection: Connection, review_note: ReviewNote, sub_program_id: int):
    query: str = """
                    INSERT INTO public.review_note (
                        sub_program,
                        reference,
                        title,
                        reference,
                        description,
                        date_raised,
                        raised_by,
                        action_owner,
                        resolution_summary,
                        resolution_details,
                        resolved_by,
                        date_resolved,
                        decision
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);  
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                sub_program_id,
                review_note.title,
                review_note.reference,
                review_note.description,
                review_note.date_raised,
                review_note.raised_by,
                review_note.action_owner,
                review_note.resolution_summary,
                review_note.resolution_details,
                review_note.resolved_by,
                review_note.date_resolved,
                review_note.decision
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating review note {e}")

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
                    conclusion = %s,
                    prepared_by = %s::jsonb,
                    reviewed_by = %s::jsonb  WHERE id = %s; 
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
                sub_program.reviewed_by.model_dump_json(),
                sub_program.prepared_by.model_dump_json(),
                program_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating sub program procedure {e}")