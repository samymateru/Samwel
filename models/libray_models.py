from psycopg import AsyncConnection
from typing import Dict
from core.tables import Tables
from schemas.library_schemas import LibraryCategory, CreateLibraryEntry, LibraryColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
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
            .returning(LibraryColumns.LIBRARY_ID.value)
            .execute()
        )
        return builder


async def get_module_library_entry_model(
        connection: AsyncConnection,
        module_id: str,
        category: LibraryCategory
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.LIBRARY.value)
            .where(LibraryColumns.MODULE_ID.value, module_id)
            .where(LibraryColumns.CATEGORY.value, category.value)
            .fetch_all()
        )

        return builder


async def delete_libray_entry_model(
        connection: AsyncConnection,
        library_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.LIBRARY.value)
            .check_exists({LibraryColumns.LIBRARY_ID.value: library_id})
            .where({LibraryColumns.LIBRARY_ID.value: library_id})
            .returning(LibraryColumns.LIBRARY_ID.value)
            .execute()
        )

        return builder


