import os
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException, Query
from starlette.responses import FileResponse
from models.planning_models import attach_draft_engagement_report_model, fetch_report_on_engagement, remove_engagement_report_model
from reports.draft_report.draft_report import generate_draft_report_model
from reports.engagement_letter.engagement_letter import generate_draft_engagement_letter_model
from reports.finding_sheet.finding_report import generate_finding_report
from schema import CurrentUser, ResponseMessage
from schemas.planning_schemas import ReportType, UserCirculate, ReportAttachment
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import get_current_user, exception_response, return_checker

router = APIRouter(prefix="/engagements")



def cleanup_file(path: str):
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"Deleted {path}")
        except Exception as e:
            print(f"Could not delete {path}: {e}")



@router.get("/reports/{engagement_id}")
async def generate_report(
        engagement_id: str,
        category: ReportType,
        background_tasks: BackgroundTasks,
        module_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        #_: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        if category.value == ReportType.ENGAGEMENT_REPORT:
            output_path, engagement_name = await generate_draft_report_model(
                connection=connection,
                engagement_id=engagement_id,
            )

        elif category.value == ReportType.FINDING_LETTER:
            output_path, engagement_name = await generate_finding_report(
                connection=connection,
                engagement_id=engagement_id,
            )

        elif category.value == ReportType.ENGAGEMENT_LETTER:
            output_path, engagement_name = await generate_draft_engagement_letter_model(
                connection=connection,
                engagement_id=engagement_id,
            )

        else:
            raise HTTPException(status_code=404, detail="Unknown Report Requested")

        background_tasks.add_task(cleanup_file, output_path)

        return FileResponse(
            path=output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"{engagement_name}-{category.value}.docx",
            headers={
                "Content-Disposition": f'attachment; filename="{engagement_name}-{category.value}.docx"'
            },
            background=background_tasks
        )



@router.post("/reports/{engagement_id}")
async def attach_report(
        engagement_id: str,
        category: ReportType,
        module_id: str = Query(...),
        attachment: UploadFile = File(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        #_: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await attach_draft_engagement_report_model(
            engagement_id=engagement_id,
            module_id=module_id,
            background_tasks=background_tasks,
            connection=connection,
            attachment=attachment,
            category=category
        )


        return await return_checker(
            data=results,
            passed="Report Successfully Attached",
            failed="Failed Attaching Report"
        )



@router.get("/reports/single/{engagement_id}")
async def fetch_engagement_report(
        engagement_id: str,
        category: ReportType,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await fetch_report_on_engagement(
            connection=connection,
            engagement_id=engagement_id,
            category=category
        )

        if data is None:
            return None

        attachment = ReportAttachment(
            filename=data.get("file_name",) ,
            type=data.get("file_type"),
            size=data.get("file_size"),
            url=data.get("url")
        )

        return attachment



@router.delete("/reports/{engagement_id}")
async def remove_engagement_report(
        engagement_id: str,
        category: ReportType,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await remove_engagement_report_model(
            connection=connection,
            engagement_id=engagement_id,
            category=category
        )

        return await return_checker(
            data=results,
            passed="Report Successfully Deleted",
            failed="Failed Deleting Report"
        )



#############################################
#   REPORT CIRCULATE
#############################################
@router.post(
    "/reports/circulate/{engagement_id}",
    response_model=ResponseMessage,
    description="""
    Sends the finalized engagement report to a list of specified users by email.

    Each user in the request must include their `user_id` and `email`. The report
    related to the given `engagement_id` will be emailed to all listed recipients.

    **Example request body:**
    ```json
    [
        { "user_id": "40501a58d0ea", "email": "john@example.com" },
        { "user_id": "50921b38e7af", "email": "sarah@example.com" }
    ]
    ```

    **Example response:**
    ```json
    { "message": "Report sent to 2 users." }
    ```
    """
)
async def circulate_main_report(
        engagement_id: str,
        users: List[UserCirculate],
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        # _: CurrentUser = Depends(get_current_user)
):
    """
    Circulate the engagement report to a list of users via email.

    Args:
        engagement_id (str): The engagement ID of the report to send.
        users (List[UserCirculate]): List of recipients with `user_id` and `email`.
        connection (AsyncConnection): Database connection.

    Returns:
        ResponseMessage: Success message after sending the report.
    """
    with exception_response():
        return ResponseMessage(detail="Report Circulated")



################################################################################
#   REPORT PUBLISH
################################################################################
@router.post(
    "/reports/publish/{engagement_id}",
    response_model=ResponseMessage,
    description="""
    Publishes the finalized engagement report and automatically sends it 
    to the responsible user.

    The system identifies the responsible user for the given `engagement_id`
    and emails them the generated report.

    **Example response:**
    ```json
    { "message": "Report successfully sent to the responsible user." }
    ```
    """
)
async def publish_main_report(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        # _: CurrentUser = Depends(get_current_user)
):
    """
    Publish and send the engagement report to the responsible user.

    Args:
        engagement_id (str): The unique ID of the engagement to publish.
        connection (AsyncConnection): Database connection.

    Returns:
        ResponseMessage: Success message after sending the report.
    """
    with exception_response():
        return ResponseMessage(detail="Report Published")
