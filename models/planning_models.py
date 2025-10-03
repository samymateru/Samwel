from fastapi import UploadFile
from psycopg import AsyncConnection
from utils import exception_response




async def attach_draft_engagement_report_model(
        connection: AsyncConnection,
        attachment: UploadFile,
        engagement_id: str,
        module_id: str
):
    with exception_response():
        pass



async def attach_finding_report_model(
        connection: AsyncConnection,
        attachment: UploadFile,
        engagement_id: str,
        module_id: str
):
    with exception_response():
        pass



async def attach_engagement_letter_model(
        connection: AsyncConnection,
        attachment: UploadFile,
        engagement_id: str,
        module_id: str
):
    with exception_response():
        pass

