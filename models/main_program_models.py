from typing import List

from fastapi import HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from models.sub_program_models import import_sub_program_from_library_model
from schemas.main_program_schemas import NewMainProgram, UpdateMainProgram, UpdateMainProgramProcessRating, \
    CreateMainProgram, MainProgramColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from core.queries import querying_main_program_data

async def create_new_main_audit_program_model(
        connection: AsyncConnection,
        main_program: NewMainProgram,
        engagement_id: str,
        throw: bool = True
):
    with exception_response():
        __main__program__ = CreateMainProgram(
            id=get_unique_key(),
            engagement=engagement_id,
            name=main_program.name,
            description=main_program.description
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .values(__main__program__)
            .into_table(Tables.MAIN_PROGRAM.value)
            .check_exists({MainProgramColumns.NAME.value: main_program.name})
            .check_exists({MainProgramColumns.ENGAGEMENT.value: engagement_id})
            .throw_error_on_exists(throw)
            .returning(MainProgramColumns.ID.value)
            .execute()
        )

        return builder


async def fetch_main_programs_models(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MAIN_PROGRAM.value)
            .where(MainProgramColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )

        return builder


async def update_main_audit_program_models(
        connection: AsyncConnection,
        main_program: UpdateMainProgram,
        program_id: str
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.MAIN_PROGRAM.value)
            .values(main_program)
            .check_exists({MainProgramColumns.ID.value: program_id })
            .where({MainProgramColumns.ID.value: program_id})
            .returning(MainProgramColumns.ID.value)
            .execute()
        )

        return builder


async def update_main_audit_program_process_rating_model(
        connection: AsyncConnection,
        main_program: UpdateMainProgramProcessRating,
        program_id: str
):
    with exception_response():

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.MAIN_PROGRAM.value)
            .values(main_program)
            .check_exists({MainProgramColumns.ID.value: program_id })
            .where({MainProgramColumns.ID.value: program_id})
            .returning(MainProgramColumns.ID.value)
            .execute()
        )

        return builder



async def delete_main_audit_program_model(
        connection: AsyncConnection,
        program_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.MAIN_PROGRAM.value)
            .check_exists({MainProgramColumns.ID.value: program_id})
            .where({MainProgramColumns.ID.value: program_id})
            .execute()
        )

        return builder


async def export_main_audit_program_to_library_model(
        connection: AsyncConnection,
        program_id: str
):
    with exception_response():
        async with connection.cursor() as cursor:
            await cursor.execute(querying_main_program_data, (program_id, ))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
            return result[0]



async def import_main_audit_program_to_library_model(
        connection: AsyncConnection,
        engagement_id: str,
        module_id: str,
        main_programs: List
):
    with exception_response():
        for main_program in main_programs:

            __main_program__ = NewMainProgram(
                name=main_program.get("data").get("program_name") or "",
                description=main_program.get("data").get("program_description") or "",
            )

            main_program_data = await create_new_main_audit_program_model(
                connection=connection,
                main_program=__main_program__,
                engagement_id=engagement_id,
                throw=False
            )


            if main_program_data.get("exists"):
                continue


            for sub_program in main_program.get("data").get("sub_programs"):
                results = await import_sub_program_from_library_model(
                    connection=connection,
                    program_id=main_program_data.get("id"),
                    sub_program=sub_program,
                    module_id=module_id
                )

                if results is None:
                    raise HTTPException(
                        status_code=400,
                        detail="Error While Import Main Program, Attach Sub Program Failed"
                    )


        return True