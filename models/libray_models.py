from psycopg import AsyncConnection
from typing import Dict

from core.tables import Tables
from schemas.library_schemas import LibraryCategory, CreateLibraryEntry
from services.connections.postgres.insert import InsertQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def create_new_libray_entry_model(
        connection: AsyncConnection,
        library: Dict,
        module_id: str,
        user_id: str,
        category: LibraryCategory
):
    with exception_response():
        __library__ = CreateLibraryEntry(
            library_id=get_unique_key(),
            module_id=module_id,
            name="",
            category=category.value,
            data=library,
            created_by=user_id,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.LIBRARY.value)
            .values(__library__)
            .check_exists({})
        )



async def get_module_library_entry_model(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        pass


async def delete_libray_entry_model(
        connection: AsyncConnection,
        library_id: str
):
    with exception_response():
        pass


