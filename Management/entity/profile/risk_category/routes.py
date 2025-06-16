from fastapi import Depends, APIRouter

from Management.entity.profile.impact_category.schemas import CombinedImpactCategory
from schema import CurrentUser
from utils import get_current_user, get_async_db_connection
from Management.entity.profile.risk_category.databases import *

router = APIRouter(prefix="/profile")

@router.get("/risk_category/{entity_id}", response_model=List[CombinedRiskCategory])
async def fetch_combined_risk_category(
        entity_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_combined_risk_category(db, company_id=entity_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)