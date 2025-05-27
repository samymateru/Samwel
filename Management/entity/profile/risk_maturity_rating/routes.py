from fastapi import APIRouter, Depends
from Management.entity.profile.risk_maturity_rating.databases import *
from schema import CurrentUser, ResponseMessage
from utils import get_current_user, get_async_db_connection
from typing import List


router = APIRouter(prefix="/profile/risk_maturity_rating")

@router.post("/", response_model=ResponseMessage)
async def create_risk_maturity_rating(
        maturity_rating: RiskMaturityRating,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await new_risk_maturity_rating(
            connection=db,
            maturity_rating=maturity_rating,
            company_id=user.entity_id)
        return ResponseMessage(detail="Risk maturity rating added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=RiskMaturityRating)
async def fetch_company_risk_maturity_rating(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_risk_maturity_rating(db, company_id=user.company_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Risk maturity rating not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/", response_model=ResponseMessage)
async def update_risk_maturity_rating(
        maturity_rating: RiskMaturityRating,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_risk_maturity_rating(
            connection=db,
            maturity_rating=maturity_rating,
            company_id=user.company_id)
        return ResponseMessage(detail="Risk maturity rating updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{maturity_rating_id}", response_model=ResponseMessage)
async def remove_risk_maturity_rating(
        maturity_rating_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await delete_risk_maturity_rating(connection=db, maturity_rating_id=maturity_rating_id)
        return ResponseMessage(detail="Risk maturity rating deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)