from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user
from Management.companies.profile.control_weakness_rating.databases import *
from Management.companies.profile.control_weakness_rating.schemas import *
from typing import List

router = APIRouter(prefix="/profile/control_weakness_rating")

@router.post("/", response_model=ResponseMessage)
def create_issue_implementation(
        control_weakness_rating: ControlWeaknessRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_control_weakness_rating(db, control_weakness_rating=control_weakness_rating, company_id=user.company_id)
        return {"detail": "Control weakness rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=List[ControlWeaknessRating])
def fetch_company_control_weakness_rating(
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_control_weakness_rating(db, company_id=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{control_weakness_rating_id}", response_model=ControlWeaknessRating)
def fetch_control_weakness_rating(
        control_weakness_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_control_weakness_rating(db, control_weakness_rating_id=control_weakness_rating_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{control_weakness_rating_id}", response_model=ResponseMessage)
def update_control_weakness_rating(
        control_weakness_rating_id: int,
        control_weakness_rating: ControlWeaknessRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_control_weakness_rating(
            db,
            control_weakness_rating=control_weakness_rating,
            control_weakness_rating_id=control_weakness_rating_id)
        return {"detail": "Control weakness rating updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{control_weakness_rating_id}", response_model=ResponseMessage)
def remove_control_weakness_rating(
        control_weakness_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_control_weakness_rating(db, control_weakness_rating_id=control_weakness_rating_id)
        return {"detail": "Control weakness rating deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)