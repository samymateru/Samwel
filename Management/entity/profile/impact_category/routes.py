from fastapi import APIRouter, Depends
from utils import get_current_user, get_async_db_connection
from schema import *
from Management.entity.profile.impact_category.databases import *

router = APIRouter(prefix="/profile")


@router.get("/impact_category/{entity_id}", response_model=List[CombinedImpactCategory])
async def fetch_combined_impact_category(
        entity_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_combined_impact_category(connection=db, company_id=entity_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



