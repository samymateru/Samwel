from fastapi import UploadFile, BackgroundTasks
from psycopg import AsyncConnection

from core.utils import upload_attachment
from models.attachment_model import add_new_attachment
from schemas.attachement_schemas import AttachmentCategory
from utils import exception_response




async def attach_draft_engagement_report_model(
        connection: AsyncConnection,
        attachment: UploadFile,
        engagement_id: str,
        module_id: str,
        background_tasks: BackgroundTasks
):
    with exception_response():

        url = upload_attachment(
            category=AttachmentCategory.DRAFT_AUDIT_REPORT,
            background_tasks=background_tasks,
            file=attachment
        )

        results = await add_new_attachment(
            connection=connection,
            attachment=attachment,
            item_id=engagement_id,
            module_id=module_id,
            url=url,
            category=AttachmentCategory.ANNUAL_PLAN
        )





async def attach_finding_report_model(
        connection: AsyncConnection,
        attachment: UploadFile,
        engagement_id: str,
        module_id: str,
        background_tasks: BackgroundTasks

):
    with exception_response():
        pass



async def attach_engagement_letter_model(
        connection: AsyncConnection,
        attachment: UploadFile,
        engagement_id: str,
        module_id: str,
        background_tasks: BackgroundTasks
):
    with exception_response():
        pass

