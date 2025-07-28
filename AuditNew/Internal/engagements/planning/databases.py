from AuditNew.Internal.engagements.attachments.schemas import Attachment
from AuditNew.Internal.engagements.planning.schemas import *
from utils import get_next_reference
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.control.databases import *
from psycopg import AsyncConnection, sql
import json
from psycopg.errors import ForeignKeyViolation, UniqueViolation


def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

async def add_engagement_letter(connection: AsyncConnection, letter: EngagementLetter, engagement_id: str):
    query = sql.SQL(
        """
            UPDATE public.engagement_letter
            SET 
            name = %s,
            value = %s,
            size = %s,
            extension = %s
            WHERE engagement = %s AND type = %s; 

        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                letter.name,
                letter.value,
                letter.size,
                letter.extension,
                engagement_id,
                "final"
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
                residue_risk,
                type
           ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="PRCM", filters={
                "risk": prcm.risk,
                "control": prcm.control,
                "engagement": engagement_id
            })
            if exists:
                raise HTTPException(status_code=400, detail="PRCM already exists")
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                prcm.process,
                prcm.risk,
                prcm.risk_rating,
                prcm.control,
                prcm.control_objective,
                prcm.control_type,
                prcm.residue_risk,
                "planning"
            ))
        await connection.commit()
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement PRCM {e}")

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

async def work_program_(connection: AsyncConnection, work_program: PlanningWorkProgram, engagement_id: str):
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
            program = MainProgram(
                name=work_program.program_name
            )

            sub_program = NewSubProgram(
                title=work_program.procedure_name
            )

            program_id = await add_new_main_program(
                connection=connection,
                program=program,
                engagement_id=engagement_id,
                callee=False
            )

            procedure = await add_new_sub_program(
                connection=connection,
                sub_program=sub_program,
                program_id=program_id,
                callee=False
            )

            await cursor.execute(query, (procedure[0], procedure[1], work_program.prcm_id))
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

async def get_prcm(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("""SELECT * from public."PRCM" WHERE engagement = %s AND type='planning';""")
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
    query = sql.SQL(
        """
        SELECT
        proc.reference,
        proc.title as procedure,
        proc.id as procedure_id,
         prog.name as program,
        prcm.process,
        prcm.risk,
        prcm.risk_rating,
        prcm.control,
        prcm.control_type
        from public."PRCM" prcm
        JOIN sub_program proc ON prcm.summary_audit_program = proc.id
        JOIN main_program prog ON proc.program = prog.id
        WHERE 
        prcm.engagement = %s AND 
        prcm.type ='planning' AND 
        prcm.reference IS NOT NULL;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
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
        UPDATE public.std_template
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
            if std_template.reviewed_by.id == "0" or std_template.reviewed_by.name == "":
                await cursor.execute(update_procedure_status, ("In progress", procedure_id))
            else:
                await cursor.execute(update_procedure_status, ("Completed", procedure_id))
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

async def edit_summary_audit_finding(connection: AsyncConnection):
    query = sql.SQL(
        """
        """)
    try:
        async with connection.cursor() as cursor:
            print(query, cursor)

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating summary of audit program {e}")

async def attach_procedure(connection: AsyncConnection, procedure_id:str, prcm_id:str):
    query = sql.SQL(
        """
        UPDATE public."PRCM" 
        SET
        summary_audit_program = %s
        WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (procedure_id, prcm_id))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error attaching risk control {e}")


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

async def review_std_template(connection: AsyncConnection, procedure: PreparedReviewedBy, procedure_id: str, resource: str):
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
