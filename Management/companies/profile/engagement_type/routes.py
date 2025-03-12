from fastapi import APIRouter, Depends
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user
from Management.companies.profile.engagement_type.databases import *
from typing import List

router = APIRouter(prefix="/profile/engagement_type")

@router.post("/{company_id}", response_model=ResponseMessage)
def create_engagement_type(
        company_id: int,
        engagement_type: EngagementType,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_engagement_type(db, engagement_type=engagement_type, company_id=company_id)
        return {"detail": "Engagement type added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/company/{company_id}", response_model=List[EngagementType])
def fetch_company_engagement_type(
        company_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_engagement_type(db, company_id=company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{engagement_type_id}", response_model=EngagementType)
def fetch_control_weakness_rating(
        engagement_type_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_type(db, engagement_type_id=engagement_type_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{engagement_type_id}", response_model=ResponseMessage)
def update_control_weakness_rating(
        engagement_type_id: int,
        engagement_type: EngagementType,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_engagement_type(
            db,
            engagement_type=engagement_type,
            engagement_type_id=engagement_type_id)
        return {"detail": "Engagement type updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{engagement_type_id}", response_model=ResponseMessage)
def remove_engagement_type(
        engagement_type_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_engagement_type(db, engagement_type_id=engagement_type_id)
        return {"detail": "Engagement type deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)