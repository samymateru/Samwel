from typing import Dict
from psycopg import AsyncConnection

from core.tables import Tables
from schemas.main_program_schemas import NewMainProgram, UpdateMainProgram, UpdateMainProgramProcessRating, \
    CreateMainProgram, MainProgramColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def create_new_main_audit_program_model(
        connection: AsyncConnection,
        main_program: NewMainProgram,
        engagement_id: str
):
    with exception_response():
        __main__program__ = CreateMainProgram(
            id=get_unique_key(),
            engagement=engagement_id,
            name=main_program.name,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .values(__main__program__)
            .into_table(Tables.MAIN_PROGRAM.value)
            .check_exists({MainProgramColumns.NAME.value: main_program.name})
            .check_exists({MainProgramColumns.ENGAGEMENT.value: engagement_id})
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


async def fetch_main_programs_combine_with_sub_programs_models(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        pass


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
        data: Dict,
        module_id: str
):
    with exception_response():
        pass

