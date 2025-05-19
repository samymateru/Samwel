from AuditNew.Internal.engagements.planning.schemas import *
from utils import get_next_reference, get_unique_key
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.risk.databases import *
from AuditNew.Internal.engagements.control.databases import *
from psycopg import AsyncConnection, sql
import json
from psycopg.errors import ForeignKeyViolation, UniqueViolation


def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

async def add_engagement_letter(connection: AsyncConnection, letter: EngagementLetter, engagement_id: str):
    query = sql.SQL(
        """
           INSERT INTO public.engagement_letter (
                id,
                engagement,
                name,
                date_attached,
                attachment
           ) 
        VALUES(%s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                letter.name,
                letter.date_attached,
                letter.attachment
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement letter {e}")

async def add_engagement_prcm(connection: AsyncConnection, prcm: PRCM, engagement_id: str):
    query = sql.SQL(
        """
           INSERT INTO public."PRCM" (
                id,
                engagement,
                process,
                risk,
                risk_rating,
                control,
                control_objective,
                control_type,
                residue_risk
           ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                prcm.process,
                prcm.risk,
                prcm.risk_rating,
                prcm.control,
                prcm.control_objective,
                prcm.control_type,
                prcm.residue_risk
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement PRCM {e}")

async def add_summary_audit_program(connection: AsyncConnection, summary: SummaryAuditProgram, engagement_id: str, prcm_id: str):
    program_id_ = 0
    procedure_id = 0
    risk_id_ = 0
    control_id_ = 0
    query = sql.SQL(
        """
            INSERT INTO public.summary_audit_program (
            id,
            engagement,
            prcm,
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
       ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            check_program_query = sql.SQL("SELECT name, id FROM public.main_program WHERE name = %s AND engagement = %s;")
            check_sub_program = sql.SQL("SELECT title, id from public.sub_program WHERE program = %s AND title = %s")
            await cursor.execute(check_program_query, (summary.program, engagement_id))
            program_rows = await cursor.fetchall()
            program_column_names = [desc[0] for desc in cursor.description]
            program_data = [dict(zip(program_column_names, row_)) for row_ in program_rows]
            if program_data.__len__() != 0: # the program exists check for the procedure
                await cursor.execute(check_sub_program, (program_data[0].get("id"), summary.procedure))
                procedure_rows = await cursor.fetchall()
                procedure_column_names = [desc[0] for desc in cursor.description]
                procedure_data = [dict(zip(procedure_column_names, row_)) for row_ in procedure_rows]
                if procedure_data.__len__() != 0:# procedure exists attach risk
                    sub_program_id = procedure_data[0].get("id")
                    risk = Risk(
                        name=summary.risk,
                        rating=summary.risk_rating
                    )
                    risk_id = await add_new_risk(connection=connection, risk=risk, sub_program_id=sub_program_id)
                    control = Control(
                        name=summary.control,
                        objective=summary.control_objective,
                        type=summary.control_type
                    )
                    control_id = await add_new_control(connection=connection, control=control, sub_program_id=sub_program_id)
                    program_id_ = program_data[0].get("id")
                    procedure_id = sub_program_id
                    risk_id_ = risk_id
                    control_id_ = control_id

                else: # procedure does not exist attach procedure the ris and control
                    program_id = program_data[0].get("id")
                    sub_program = NewSubProgram(
                        title=summary.procedure
                    )
                    sub_program_id = await add_new_sub_program(connection=connection, sub_program=sub_program,
                                                         program_id=program_id)
                    risk = Risk(
                        name=summary.risk,
                        rating=summary.risk_rating
                    )
                    risk_id = await add_new_risk(connection=connection, risk=risk, sub_program_id=sub_program_id)
                    control = Control(
                        name=summary.control,
                        objective=summary.control_objective,
                        type=summary.control_type
                    )
                    control_id = await add_new_control(connection=connection, control=control, sub_program_id=sub_program_id)
                    program_id_ = program_id
                    procedure_id = sub_program_id
                    risk_id_ = risk_id
                    control_id_ = control_id

            else: # program does not exist
                program = MainProgram(
                    name=summary.program
                )
                program_id = await add_new_main_program(connection=connection, program=program, engagement_id=engagement_id)
                sub_program = NewSubProgram(
                    title=summary.procedure
                )
                sub_program_id = await add_new_sub_program(connection=connection, sub_program=sub_program, program_id=program_id)
                risk = Risk(
                    name=summary.risk,
                    rating=summary.risk_rating
                )
                risk_id = await add_new_risk(connection=connection, risk=risk, sub_program_id=sub_program_id)
                control = Control(
                    name=summary.control,
                    objective=summary.control_objective,
                    type=summary.control_type
                )
                control_id = await add_new_control(connection=connection, control=control, sub_program_id=sub_program_id)
                program_id_ = program_id
                procedure_id = sub_program_id
                risk_id_ = risk_id
                control_id_ = control_id

            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                prcm_id,
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
            summary_audit_program_id = await cursor.fetchone()
            await cursor.execute("""UPDATE public."PRCM" SET summary_audit_program = %s WHERE id = %s""", (
                summary_audit_program_id[0],
                prcm_id
                ))
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
                type,
                prepared_by,
                reviewed_by
           ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                data["type"],
                None,
                None
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

async def get_prcm(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("""SELECT * from public."PRCM" WHERE engagement = %s""")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement PRCM {e}")

async def get_engagement_letter(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.engagement_letter WHERE engagement = %s")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement letter {e}")

async def get_summary_audit_program(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.summary_audit_program WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of audit program {e}")

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

    update_procedure_status = sql.SQL(
        """
        UPDATE public.sub_program
        SET 
        status = %s
        WHERE id = %s; 
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
            if std_template.prepared_by.id != "" or std_template.prepared_by.name != "":
                await cursor.execute(update_procedure_status, ("Completed", procedure_id))
            else:
                await cursor.execute(update_procedure_status, ("In progress", procedure_id))
            await connection.commit()

    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Planning procedure already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating planning procedure {e}")

async def edit_prcm(connection: AsyncConnection, prcm: PRCM, prcm_id: str):
    query = sql.SQL(
        """
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
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                prcm.process,
                prcm.risk,
                prcm.risk_rating,
                prcm.control,
                prcm.control_objective,
                prcm.control_type,
                prcm.residue_risk,
                prcm_id))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating prcm {e}")

async def remove_prcm(connection: AsyncConnection, prcm_id: str):
    query = sql.SQL("""DELETE FROM public."PRCM" WHERE id = %s;""")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (prcm_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting prcm {e}")

async def remove_summary_audit_program(connection: AsyncConnection, summary_audit_program_id: str):
    query = sql.SQL("DELETE FROM public.summary_audit_program id = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (summary_audit_program_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting summary of audit program {e}")

async def edit_summary_audit_finding(connection: AsyncConnection, summary: SummaryAuditProgram, summary_audit_program_id: str):
    query = sql.SQL(
        """
           UPDATE public.summary_audit_program 
           SET
           process = %s,
           risk = %s,
           risk_rating = %s,
           control = %s,
           procedure = %s,
           program = %s
           WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            query_prog_id = sql.SQL("SELECT prog_id FROM public.summary_audit_program WHERE id = %s")
            await cursor.execute(query_prog_id, (summary_audit_program_id,))
            summary_data = await cursor.fetchall()[0][0]
            risk = Risk(
                name=summary.risk,
                rating=summary.risk_rating
            )
            #await edit_risk(connection=connection, risk=risk, )
            await cursor.execute(query, (
                summary.process,
                summary.risk,
                summary.risk_rating,
                summary.control,
                summary.procedure,
                summary.program,
                summary_audit_program_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating summary of audit program {e}")


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
            results = %s::jsonb,
            observation = %s::jsonb,
            conclusion = %s::jsonb
            WHERE id = %s; 
        """).format(resource=sql.Identifier('public', procedure_types.get(resource)))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                safe_json_dump(procedure.tests),
                safe_json_dump(procedure.results),
                safe_json_dump(procedure.observation),
                safe_json_dump(procedure.conclusion),
                procedure_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving procedure {e}")
