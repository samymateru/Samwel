from fastapi import HTTPException
from AuditNew.Internal.engagements.work_program.schemas import *
from utils import get_unique_key
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation


def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

async def add_new_main_program(connection: AsyncConnection, program: MainProgram, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.main_program (id, engagement, name, status) 
        VALUES (%s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                get_unique_key(),
                engagement_id,
                program.name,
                "Not Started"
            ))
            main_program_id = await cursor.fetchone()
            await connection.commit()
            return main_program_id[0]
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Main program already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating main program {e}")

async def add_new_sub_program(connection: AsyncConnection, sub_program: NewSubProgram, program_id: str):
    check_module_id_query = sql.SQL(
        """
        SELECT cm.procedure_reference AS reference, cm.id
        FROM modules cm
        JOIN annual_plans ap ON ap.module = cm.id
        JOIN engagements e ON e.plan_id = ap.id
        JOIN main_program mp ON mp.engagement = e.id
        WHERE mp.id = {program_id};
        """).format(program_id=sql.Literal(program_id))

    update_module_id_query = sql.SQL(
        """
        UPDATE public.modules
        SET 
        procedure_reference = %s
        WHERE id = %s
        """)

    query = sql.SQL(
        """
        INSERT INTO public.sub_program (
        id,
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
        prepared_by,
        status
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(check_module_id_query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            reference = [dict(zip(column_names, row_)) for row_ in rows]
            count = reference[0].get("reference")
            if count is None:
                count = 1
                prefix = f"PROC-{count:04d}"

            else:
                count = int(count) + 1
                prefix = f"PROC-{count:05d}"

            await cursor.execute(update_module_id_query, (count, reference[0].get("id")))
            
            await cursor.execute(query,(
                get_unique_key(),
                program_id,
                prefix,
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
                "",
                None,
                None,
                "Pending"
            ))
            sub_program_id = await cursor.fetchone()
            await connection.commit()
            return sub_program_id[0]
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Main program id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Sub program already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating sub program {e}")

async def add_new_sub_program_evidence(connection: AsyncConnection, evidence: SubProgramEvidence, sub_program_id: str):
    query = sql.SQL(
    """
       INSERT INTO public.sub_program_evidence (
           id,
           sub_program,
           attachment
           ) 
    VALUES (%s, %s, %s); 
    """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                sub_program_id,
                evidence.attachment
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating sub program evidence {e}")

async def get_sub_program_evidence(connection: AsyncConnection, sub_program_id: str):
    query = sql.SQL("SELECT * from public.sub_program_evidence WHERE sub_program = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (sub_program_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching sub program evidence {e}")

async def get_main_program(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.main_program WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching main program {e}")

async def get_sub_program(connection: AsyncConnection, program_id: str):
    query = sql.SQL("SELECT * FROM public.sub_program WHERE program = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (program_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching sub program {e}")

async def get_sub_program_(connection: AsyncConnection, sub_program_id: str):
    query = sql.SQL("SELECT * FROM public.sub_program WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (sub_program_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching sub program {e}")

async def remove_work_program(connection: AsyncConnection, id: str, table: str, resource: str):
    query = sql.SQL("DELETE FROM {table} WHERE id = %s").format(table=sql.Identifier('public', table))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting {resource} {e}")

async def edit_sub_program(connection: AsyncConnection, sub_program: SubProgram, sub_program_id: str):
    query = sql.SQL(
        """
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
        prepared_by = %s::jsonb,
        reviewed_by = %s::jsonb,
        conclusion = %s WHERE id = %s; 
        """)
    update_procedure_status = sql.SQL(
        """
        UPDATE public.sub_program
        SET 
        status = %s
        WHERE id = %s; 
        """)
    try:
        prepared_by = None if sub_program.prepared_by is None else sub_program.prepared_by.model_dump_json()
        reviewed_by = None if sub_program.reviewed_by is None else sub_program.reviewed_by.model_dump_json()
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
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
                prepared_by,
                reviewed_by,
                sub_program.conclusion,
                sub_program_id
            ))
            await connection.commit()
            if sub_program.reviewed_by is None:
                await cursor.execute(update_procedure_status, ("In progress", sub_program_id))
            else:
                await cursor.execute(update_procedure_status, ("Completed", sub_program_id))
            await connection.commit()

    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Sub program already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating sub program procedure {e}")

async def edit_main_program(connection: AsyncConnection, program: MainProgram, program_id: str):
    query = sql.SQL(
        """
        UPDATE public.main_program
        SET 
        name = %s
        WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (program.name, program_id))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Main program already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating main program {e}")

async def get_work_program(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        SELECT
          main_program.id,
          main_program.name,
          json_agg(
            json_build_object(
              'procedure_id', sub_program.id,
              'reference', sub_program.reference,
              'procedure_title', sub_program.title
            )
          ) AS procedures
        FROM
          main_program
        LEFT JOIN sub_program ON sub_program.program = main_program.id
        WHERE
          main_program.engagement = %s
        GROUP BY
          main_program.id, main_program.name
        ORDER BY
          main_program.name;
        """
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching work program {e}")

async  def add_new_sub_program_risk_control(connection: AsyncConnection, risk_control: RiskControl, sub_program_id: str, engagement_id: str):
    query = sql.SQL(
        """
           INSERT INTO public."PRCM" (
                id,
                engagement,
                risk,
                risk_rating,
                control,
                control_objective,
                control_type,
                residue_risk,
                type,
                summary_audit_program
           ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                risk_control.risk,
                risk_control.risk_rating,
                risk_control.control,
                risk_control.control_objective,
                risk_control.control_type,
                risk_control.residue_risk,
                "program",
                sub_program_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding sub procedure risk control {e}")

async def get_sub_program_risk_control(connection: AsyncConnection, sub_program_id: str):
    query = sql.SQL(
        """
        SELECT * from public."PRCM" WHERE summary_audit_program={procedure_id}
        """).format(procedure_id=sql.Literal(sub_program_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching sub program risk control {e}")

##########################################################################################################
async def save_sub_program_(connection: AsyncConnection, sub_program: SaveWorkProgramProcedure, sub_program_id: str):
    query = sql.SQL(
        """
        UPDATE public.sub_program
        SET 
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
        conclusion = %s 
        WHERE id = %s; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
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
                sub_program_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving sub program procedure {e}")

async def edit_work_program_procedure_prepared(connection: AsyncConnection, sub_program: PreparedReviewedBy, sub_program_id: str):
    query = sql.SQL(
        """
            UPDATE public.sub_program
            SET 
            prepared_by = %s::jsonb
            WHERE id = %s; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                sub_program.model_dump_json(),
                sub_program_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error prepared procedure {e}")

async def edit_work_program_procedure_reviewed(connection: AsyncConnection, sub_program: PreparedReviewedBy, sub_program_id: str):
    query = sql.SQL(
        """
            UPDATE public.sub_program
            SET 
            reviewed_by = %s::jsonb
            WHERE id = %s; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                sub_program.model_dump_json(),
                sub_program_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error review procedure {e}")