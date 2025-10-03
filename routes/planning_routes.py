from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from starlette.responses import FileResponse
from models.planning_models import attach_draft_engagement_report_model
from reports.draft_report.draft_report import generate_draft_report_model
from reports.engagement_letter.engagement_letter import generate_draft_engagement_letter_model
from reports.finding_sheet.finding_report import generate_finding_report
from schema import CurrentUser
from schemas.planning_schemas import ReportType
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import get_current_user, exception_response, return_checker

router = APIRouter(prefix="/engagements")

@router.post("/planning/draft_audit_report/{engagement_id}")
async def generate_draft_engagement_report(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await generate_draft_report_model(
            connection=connection,
            engagement_id=engagement_id,
            module_id=auth.module_id
        )

        return FileResponse(
            path=data[0],
            filename=f"{data[1]}-draft-report.docx",
        )


@router.post("/planning/draft_engagement_letter/{engagement_id}")
async def generate_draft_engagement_letter_report(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        #_: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await generate_draft_engagement_letter_model(
            connection=connection,
            engagement_id=engagement_id,
            module_id=""
        )

        return FileResponse(
            path=data[0],
            filename=f"{data[1]}-draft-engagement-letter-report.docx",
        )



@router.post("/planning/finding_sheet/{engagement_id}")
async def generate_finding_sheet_report(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await generate_finding_report(
            connection=connection,
            engagement_id=engagement_id,
            module_id=auth.module_id
        )

        return FileResponse(
            path=data[0],
            filename=f"{data[1]}-finding-report.docx",
        )


# End of Generation




@router.post("/planning/attach/{engagement_id}")
async def attach_report(
        engagement_id: str,
        category: ReportType,
        attachment: UploadFile = File(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await attach_draft_engagement_report_model(
            engagement_id=engagement_id,
            module_id=auth.module_id,
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




# data = await generate_draft_report_model(
 #            connection=connection,
 #            engagement_id="4b15ba494eb9",
 #            module_id="04e9e6ebdf06"
 #        )