from AuditNew.Internal.reports.schemas import *
from utils import get_current_user, get_async_db_connection
from schema import CurrentUser
from fastapi import APIRouter, Depends
from AuditNew.Internal.reports.databases import *

router = APIRouter(prefix="/reports")

@router.get("/master/{company_module_id}")
async def fetch_main_reports(
        company_module_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    #if user.status_code != 200:
        #raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        main_report_data = await get_main_reports(connection=db, company_module_id=company_module_id)
        if main_report_data is None:
            raise HTTPException(status_code=400, detail="No data to show")
        return main_report_data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)