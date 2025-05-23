from fastapi import APIRouter, Depends
from Management.entity.profile.risk_rating.databases import *
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user, get_async_db_connection
from typing import List

router = APIRouter(prefix="/profile/risk_rating")

@router.post("/", response_model=ResponseMessage)
def create_risk_rating(
        risk_rating: RiskRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_risk_rating(
            db,
            risk_rating=risk_rating,
            company_id=user.company_id)
        return {"detail": "Risk rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=RiskRating)
async def fetch_company_risk_rating(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_risk_rating(db, company_id=user.company_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Risk rating not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{risk_rating_id}", response_model=ResponseMessage)
def update_risk_rating(
        risk_rating_id: int,
        risk_rating: RiskRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_risk_rating(
            db,
            risk_rating=risk_rating,
            risk_rating_id=risk_rating_id)
        return {"detail", "Risk rating updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{risk_rating_id}", response_model=ResponseMessage)
def remove_risk_rating(
        risk_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        delete_risk_rating(db, risk_rating_id=risk_rating_id)
        return {"detail": "Risk rating deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

