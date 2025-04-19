from fastapi import APIRouter, Depends
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user, get_async_db_connection
from Management.companies.profile.control_effectiveness_rating.databases import *
from typing import List

router = APIRouter(prefix="/profile/control_effectiveness_rating")

@router.post("/", response_model=ResponseMessage)
def create_control_effectiveness_rating(
        control_effectiveness_rating: ControlEffectivenessRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_control_effectiveness_rating(db, control_effectiveness_rating=control_effectiveness_rating, company_id=user.company_id)
        return {"detail": "Control effectiveness rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=ControlEffectivenessRating)
async def fetch_company_control_effectiveness_rating(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_control_effectiveness_rating(db, company_id=user.company_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Effectiveness rating is not valid")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{control_effectiveness_rating_id}", response_model=ResponseMessage)
def update_control_weakness_rating(
        control_effectiveness_rating_id: int,
        control_effectiveness_rating: ControlEffectivenessRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_control_effectiveness_rating(
            db,
            control_effectiveness_rating=control_effectiveness_rating,
            control_effectiveness_rating_id=control_effectiveness_rating_id)
        return {"detail": "Control weakness rating updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{control_effectiveness_rating_id}", response_model=ResponseMessage)
def remove_control_weakness_rating(
        control_effectiveness_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_control_weakness_rating(db, control_effectiveness_rating_id=control_effectiveness_rating_id)
        return {"detail": "Control weakness rating deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)