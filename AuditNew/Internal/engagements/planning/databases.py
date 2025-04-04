from AuditNew.Internal.engagements.planning.schemas import *
from utils import get_next_reference
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.risk.databases import *
from AuditNew.Internal.engagements.control.databases import *

def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

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
    program_id_ = 0
    procedure_id = 0
    risk_id_ = 0
    control_id_ = 0
    query: str = """
                   INSERT INTO public.summary_audit_program (
                        engagement,
                        process,
                        risk,
                        risk_rating,
                        control,
                        procedure,
                        program,
                        procedure_id,
                        program_id,
                        risk_id,
                        control_id
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            check_program_query:str = """
                                         SELECT name, id FROM public.main_program WHERE name = %s AND engagement = %s;
                                        """
            check_sub_program:str = """
                                        SELECT title, id from public.sub_program WHERE program = %s AND title = %s;
                                    """
            cursor: Cursor
            cursor.execute(check_program_query, (summary.program, engagement_id))
            program_rows = cursor.fetchall()
            program_column_names = [desc[0] for desc in cursor.description]
            program_data = [dict(zip(program_column_names, row_)) for row_ in program_rows]
            if program_data.__len__() != 0: # the program exists check for the procedure
                cursor.execute(check_sub_program, (program_data[0].get("id"), summary.procedure))
                procedure_rows = cursor.fetchall()
                procedure_column_names = [desc[0] for desc in cursor.description]
                procedure_data = [dict(zip(procedure_column_names, row_)) for row_ in procedure_rows]
                if procedure_data.__len__() != 0:# procedure exists attach risk
                    sub_program_id = procedure_data[0].get("id")
                    risk = Risk(
                        name=summary.risk,
                        rating=summary.risk_rating
                    )
                    risk_id = add_new_risk(connection=connection, risk=risk, sub_program_id=sub_program_id)
                    control = Control(
                        name=summary.control,
                        objective=summary.control_objective,
                        type=summary.control_type
                    )
                    control_id = add_new_control(connection=connection, control=control, sub_program_id=sub_program_id)
                    program_id_ = program_data[0].get("id")
                    procedure_id = sub_program_id
                    risk_id_ = risk_id
                    control_id_ = control_id

                else: # procedure does not exist attach procedure the ris and control
                    program_id = program_data[0].get("id")
                    sub_program = NewSubProgram(
                        title=summary.procedure
                    )
                    sub_program_id = add_new_sub_program(connection=connection, sub_program=sub_program,
                                                         program_id=program_id)
                    risk = Risk(
                        name=summary.risk,
                        rating=summary.risk_rating
                    )
                    risk_id = add_new_risk(connection=connection, risk=risk, sub_program_id=sub_program_id)
                    control = Control(
                        name=summary.control,
                        objective=summary.control_objective,
                        type=summary.control_type
                    )
                    control_id = add_new_control(connection=connection, control=control, sub_program_id=sub_program_id)
                    program_id_ = program_id
                    procedure_id = sub_program_id
                    risk_id_ = risk_id
                    control_id_ = control_id

            else: # program does not exist
                program = MainProgram(
                    name=summary.program
                )
                program_id = add_new_main_program(connection=connection, program=program, engagement_id=engagement_id)
                sub_program = NewSubProgram(
                    title=summary.procedure
                )
                sub_program_id = add_new_sub_program(connection=connection, sub_program=sub_program, program_id=program_id)
                risk = Risk(
                    name=summary.risk,
                    rating=summary.risk_rating
                )
                risk_id = add_new_risk(connection=connection, risk=risk, sub_program_id=sub_program_id)
                control = Control(
                    name=summary.control,
                    objective=summary.control_objective,
                    type=summary.control_type
                )
                control_id = add_new_control(connection=connection, control=control, sub_program_id=sub_program_id)
                program_id_ = program_id
                procedure_id = sub_program_id
                risk_id_ = risk_id
                control_id_ = control_id

            cursor.execute(query, (
                engagement_id,
                summary.process,
                summary.risk,
                summary.risk_rating,
                summary.control,
                summary.procedure,
                summary.program,
                procedure_id,
                program_id_,
                risk_id_,
                control_id_
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding summary of audit program {e}")

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

def edit_prcm(connection: Connection, prcm: PRCM, prcm_id: int):
    query: str = """
                  UPDATE public."PRCM"
                    SET
                    process = %s,
                    risk = %s,
                    risk_rating = %s,
                    control = %s,
                    control_objective = %s,
                    control_type = %s,
                    residue_risk = %s
                  WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                prcm.process,
                prcm.risk,
                prcm.risk_rating,
                prcm.control,
                prcm.control_objective,
                prcm.control_type,
                prcm.residue_risk,
                prcm_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating prcm {e}")

def remove_prcm(connection: Connection, prcm_id: int):
    query: str = """
                  DELETE FROM public."PRCM" WHERE id = %s;
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (prcm_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting prcm {e}")

def remove_summary_audit_program(connection: Connection, summary_audit_program_id: int):
    query: str = """
                  DELETE FROM public.summary_audit_program id = %s;
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (summary_audit_program_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting summary of audit program {e}")

def edit_summary_audit_finding(connection: Connection, summary: SummaryAuditProgram, summary_audit_program_id: int):
    query: str = """
                   UPDATE public.summary_audit_program 
                   SET
                   process = %s,
                   risk = %s,
                   risk_rating = %s,
                   control = %s,
                   procedure = %s,
                   program = %s
                   WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            query_prog_id: str = """
                                  SELECT prog_id FROM public.summary_audit_program WHERE id = %s
                                 """
            cursor: Cursor
            cursor.execute(query_prog_id, (summary_audit_program_id,))
            summary_data = cursor.fetchall()[0][0]
            risk = Risk(
                name=summary.risk,
                rating=summary.risk_rating
            )
            edit_risk(connection=connection)
            cursor.execute(query, (
                summary.process,
                summary.risk,
                summary.risk_rating,
                summary.control,
                summary.procedure,
                summary.program,
                summary_audit_program_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating summary of audit program {e}")