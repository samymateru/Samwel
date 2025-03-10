from fastapi import APIRouter, Depends, HTTPException
from Management.companies.profile.risk_maturity_rating.databases import *
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user
from typing import List


router = APIRouter(prefix="/profile/risk_maturity_rating")

@router.post("/{company_id}", response_model=ResponseMessage)
def create_opinion_rating(
        company_id: int,
        maturity_rating: RiskMaturityRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_risk_maturity_rating(
            db,
            maturity_rating=maturity_rating,
            company_id=company_id)
        return {"detail": "Risk maturity rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/company/{company_id}", response_model=List[RiskMaturityRating])
def fetch_company_risk_maturity_rating(
        company_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_risk_maturity_rating(db, company_id=company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{maturity_rating_id}", response_model=RiskMaturityRating)
def fetch_risk_maturity_rating(
        maturity_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_risk_maturity_rating(db, maturity_rating_id=maturity_rating_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{maturity_rating_id}", response_model=ResponseMessage)
def update_risk_maturity_rating(
        maturity_rating_id: int,
        maturity_rating: RiskMaturityRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_risk_maturity_rating(
            db,
            maturity_rating=maturity_rating,
            maturity_rating_id=maturity_rating_id)
        return {"detail": "Risk maturity rating updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{maturity_rating_id}", response_model=ResponseMessage)
def remove_risk_maturity_rating(
        maturity_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        delete_risk_maturity_rating(db, maturity_rating_id=maturity_rating_id)
        return {"detail": "Risk maturity rating deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)