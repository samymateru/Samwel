from typing import Dict
from psycopg import AsyncConnection
from schemas.main_program_schemas import NewMainProgram, UpdateMainProgram, UpdateMainProgramProcessRating
from utils import exception_response


async def create_new_main_audit_program_model(
        connection: AsyncConnection,
        main_program: NewMainProgram,
        engagement_id: str
):
    with exception_response():
        pass


async def export_main_audit_program_to_library_model(
        connection: AsyncConnection,
        data: Dict,
        module_id: str
):
    with exception_response():
        pass


async def fetch_main_programs_models(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        pass


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
        pass


async def update_main_audit_program_process_rating_model(
        connection: AsyncConnection,
        main_program: UpdateMainProgramProcessRating,
        program_id: str
):
    with exception_response():
        pass



async def delete_main_audit_program_model(
        connection: AsyncConnection,
        program_id: str
):
    with exception_response():
        pass
