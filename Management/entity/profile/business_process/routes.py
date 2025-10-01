from fastapi import APIRouter, Depends
from utils import get_current_user, get_async_db_connection
from schema import *
from Management.entity.profile.business_process.schemas import *
from Management.entity.profile.business_process.databases import *

router = APIRouter(prefix="/profile")


@router.get("/business_process/{entity_id}", response_model=List[CombinedBusinessProcess])
async def fetch_combined_business_process(
        entity_id: str,
        db = Depends(get_async_db_connection),
        _: CurrentUser = Depends(get_current_user)
    ):
    try:
        data = await get_combined_business_process(db, company_id=entity_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


