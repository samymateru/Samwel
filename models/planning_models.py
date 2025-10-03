from datetime import datetime

from fastapi import UploadFile, BackgroundTasks, HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from core.utils import upload_attachment
from models.engagement_models import get_single_engagement_with_plan_details
from schemas.attachement_schemas import AttachmentCategory
from schemas.planning_schemas import Reports, ReportType, ReportsColumns
from services.connections.postgres.insert import InsertQueryBuilder
from utils import exception_response, get_unique_key



async def attach_draft_engagement_report_model(
        connection: AsyncConnection,
        attachment: UploadFile,
        engagement_id: str,
        module_id: str,
        category: ReportType,
        background_tasks: BackgroundTasks
):
    with exception_response():

        engagement_data = await get_single_engagement_with_plan_details(
            connection=connection,
            engagement_id=engagement_id
        )

        if engagement_data is None:
            raise HTTPException(status_code=404, detail="Engagement Not Found")


        __report__ = Reports(
            report_id=get_unique_key(),
            module_id=module_id,
            engagement_id=engagement_id,
            url=upload_attachment(
            category=AttachmentCategory.ANNUAL_PLAN,
            background_tasks=background_tasks,
            file=attachment
            ),
            plan_name=engagement_data.get("pln_name"),
            plan_year=engagement_data.get("pln_year"),
            engagement_name=engagement_data.get("name"),
            engagement_code=engagement_data.get("code"),
            file_name=attachment.filename,
            file_type=attachment.content_type,
            file_size=attachment.size,
            category=category,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.REPORTS.value)
            .values(__report__)
            .check_exists({ReportsColumns.ENGAGEMENT_NAME.value: engagement_data.get("name")})
            .check_exists({ReportsColumns.ENGAGEMENT_ID.value: engagement_data.get("id")})
            .returning(ReportsColumns.ENGAGEMENT_ID.value)
            .execute()
        )

        return builder
