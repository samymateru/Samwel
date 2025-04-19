from fastapi import APIRouter, Depends
from schema import CurrentUser
from Management.companies.profile.root_cause_category.databases import *
from utils import get_db_connection, get_current_user, get_async_db_connection

router = APIRouter(prefix="/profile")


@router.get("/root_cause_category", response_model=List[CombinedRootCauseCategory])
async def fetch_root_cause_category(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_combined_root_cause_category(db, company_id=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
