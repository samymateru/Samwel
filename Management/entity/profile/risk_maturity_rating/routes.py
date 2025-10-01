from fastapi import APIRouter, Depends
from Management.entity.profile.risk_maturity_rating.databases import *
from schema import CurrentUser, ResponseMessage
from utils import get_current_user, get_async_db_connection


router = APIRouter(prefix="/profile/risk_maturity_rating")


@router.get("/{entity_id}", response_model=RiskMaturityRating)
async def fetch_company_risk_maturity_rating(
        entity_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_risk_maturity_rating(db, company_id=entity_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Risk maturity rating not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
