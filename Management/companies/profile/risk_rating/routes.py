from fastapi import APIRouter, Depends, HTTPException
from Management.companies.profile.risk_rating.databases import *
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user
from typing import List

router = APIRouter(prefix="/profile/risk_rating")

@router.post("/{company_id}", response_model=ResponseMessage)
def create_risk_rating(
        company_id: int,
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
            company_id=company_id)
        return {"detail": "Risk rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/company/{company_id}", response_model=List[RiskRating])
def fetch_company_risk_rating(
        company_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_risk_rating(db, company_id=company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{risk_rating_id}")
def fetch_risk_rating(
        risk_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_risk_rating(db, risk_rating_id=risk_rating_id)
        return data
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

