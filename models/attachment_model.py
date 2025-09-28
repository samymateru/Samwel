from fastapi import UploadFile
from psycopg import AsyncConnection
from typing_extensions import Optional
from datetime import datetime

from core.tables import Tables
from schemas.attachement_schemas import CreateAttachment, AttachmentCategory, AttachmentColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from utils import exception_response, get_unique_key


async def add_new_attachment(
        connection: AsyncConnection,
        attachment: UploadFile,
        item_id: str,
        module_id: str,
        url: str,
        category: AttachmentCategory,
        creator: Optional[str] = None
):
    with exception_response():
        __attachment__ = CreateAttachment(
            attachment_id=get_unique_key(),
            item_id=item_id,
            module_id=module_id,
            filename=attachment.filename,
            type=attachment.content_type,
            size=attachment.size,
            url=url,
            category=category.value,
            creator=creator,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ATTACHMENTS.value)
            .values(__attachment__)
            .returning(AttachmentColumns.ATTACHMENT_ID.value)
            .execute()
        )

        return builder



async def fetch_item_attachment(
        connection: AsyncConnection,
        category: AttachmentCategory,
        item_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ATTACHMENTS.value)
            .where(AttachmentColumns.ITEM_ID.value, item_id)
            .where(AttachmentColumns.CATEGORY.value, category.value)
            .fetch_all()
        )

        return builder



async def remove_attachment(
        connection: AsyncConnection,
        attachment_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.ATTACHMENTS.value)
            .check_exists({AttachmentColumns.ATTACHMENT_ID.value: attachment_id})
            .where({AttachmentColumns.ATTACHMENT_ID.value: attachment_id})
            .returning(AttachmentColumns.ATTACHMENT_ID.value)
            .execute()

        )

        return builder
