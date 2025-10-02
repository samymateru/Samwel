from fastapi import APIRouter, Depends, Query
from starlette.responses import FileResponse

from reports.draft_report.draft_report import generate_draft_report_model
from reports.finding_sheet.finding_report import generate_finding_report
from schema import CurrentUser
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import get_current_user, exception_response

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
        module_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        #_: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        pass
        # data = await generate_draft_report_model(
        #     connection=connection,
        #     engagement_id=engagement_id,
        #     module_id="04e9e6ebdf06"
        # )
        #
        # return FileResponse(
        #     path=data[0],
        #     filename=f"{data[1]}-draft-report.docx",
        # )



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






 # data = await generate_draft_report_model(
 #            connection=connection,
 #            engagement_id="4b15ba494eb9",
 #            module_id="04e9e6ebdf06"
 #        )