from psycopg import AsyncConnection
from core.tables import Tables
from schemas.sub_program_schemas import NewSubProgram, UpdateSubProgram, CreateSubProgram, SubProgramColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key

async def create_new_sub_program_model(
        connection: AsyncConnection,
        sub_program: NewSubProgram,
        program_id: str
):
    with exception_response():
        __sub__program__ = CreateSubProgram(
            id=get_unique_key(),
            program=program_id,
            title=sub_program.title,
            observation="",
            brief_description="",
            audit_objective="",
            test_description="",
            test_type="",
            sampling_approach="",
            results_of_test="",
            extended_testing=False,
            extended_procedure="",
            extended_results="",
            effectiveness="",
            conclusion=""
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .values(__sub__program__)
            .into_table(Tables.SUB_PROGRAM.value)
            .check_exists({SubProgramColumns.TITLE.value: sub_program.title})
            .check_exists({SubProgramColumns.PROGRAM.value: program_id})
            .returning(SubProgramColumns.ID.value)
            .execute()
        )

        return builder


async def fetch_all_sub_program_model(
        connection: AsyncConnection,
        program_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.SUB_PROGRAM.value)
            .where(SubProgramColumns.PROGRAM.value, program_id)
            .fetch_all()
        )

        return builder


async def fetch_single_sub_program_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.SUB_PROGRAM.value)
            .where(SubProgramColumns.ID.value, sub_program_id)
            .fetch_one()
        )

        return builder


async def update_sub_program_model(
        connection: AsyncConnection,
        sub_program: UpdateSubProgram,
        sub_program_id: str
):
    with exception_response():

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .values(sub_program)
            .into_table(Tables.SUB_PROGRAM.value)
            .check_exists({SubProgramColumns.ID.value: sub_program_id})
            .where({SubProgramColumns.ID.value: sub_program_id})
            .returning(SubProgramColumns.ID.value)
            .execute()
        )

        return builder


async def delete_sub_program_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.SUB_PROGRAM.value)
            .check_exists({SubProgramColumns.ID.value: sub_program_id})
            .where({SubProgramColumns.ID.value: sub_program_id})
            .execute()
        )

        return builder


async def export_sub_program_to_lib_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        pass