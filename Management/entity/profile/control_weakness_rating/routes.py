from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user, get_async_db_connection
from Management.entity.profile.control_weakness_rating.databases import *
from Management.entity.profile.control_weakness_rating.schemas import *
from typing import List

router = APIRouter(prefix="/profile/control_weakness_rating")

@router.post("/", response_model=ResponseMessage)
async def create_issue_implementation(
        control_weakness_rating: ControlWeaknessRating,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await new_control_weakness_rating(db, control_weakness_rating=control_weakness_rating, company_id=user.entity_id)
        return {"detail": "Control weakness rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=ControlWeaknessRating)
async def fetch_company_control_weakness_rating(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_control_weakness_rating(db, company_id=user.company_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Weakness rating not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/", response_model=ResponseMessage)
async def update_control_weakness_rating(
        control_weakness_rating: ControlWeaknessRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_control_weakness_rating(
            connection=db,
            control_weakness_rating=control_weakness_rating,
            company_id=user.company_id
        )
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