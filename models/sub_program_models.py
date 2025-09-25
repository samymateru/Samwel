from psycopg import AsyncConnection
from schemas.sub_program_schemas import NewSubProgram, UpdateSubProgram
from utils import exception_response


async def create_new_sub_program_model(
        connection: AsyncConnection,
        sub_program: NewSubProgram,
        program_id: str
):
    with exception_response():
        pass


async def fetch_all_sub_program_model(
        connection: AsyncConnection,
        program_id: str
):
    with exception_response():
        pass


async def fetch_single_sub_program_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        pass


async def update_sub_program_model(
        connection: AsyncConnection,
        sub_program: UpdateSubProgram,
        sub_program_id: str
):
    with exception_response():
        pass


async def delete_sub_program_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        pass


async def export_sub_program_to_lib_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        pass